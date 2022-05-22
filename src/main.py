import sys

import cv2
from encoder import encode
from decoder import decode

from imutils.video import FileVideoStream
from bitstring import BitArray

import numpy as np
from util import write_buf_bytes


def main():
    macroblock_size = 16

    # Main encoding loop while reading mp4
    vs = FileVideoStream("./timelapse.mp4").start()

    i = 0
    last_frame = None

    f = open("./output.mjpeg", "wb")
    write_buf_bytes(macroblock_size, 1, f)

    while (i := i + 1) and not (frame := vs.read()) is None:
        try:
            print("frame", f"{i:0>5}")
            last_frame = encode(frame, last_frame, f, i, macroblock_size)
            print()

            if i == 10:
                break
        except Exception as e:
            print(e)
            print(f"Could not read frame {i}", file=sys.stderr)
            return

    f.close()

    print(
        """
    
    decode
    
    """
    )

    with open("./output.mjpeg", "rb") as fi:
        frames = decode(fi, n=10)

    for ii, frame in enumerate(frames):
        cv2.imwrite(f"out/frame_{ii:0>4}.jpeg", frame)


if __name__ == "__main__":
    main()
