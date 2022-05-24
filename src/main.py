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
    vs = FileVideoStream("./hyperlapse.mp4").start()

    i = 0
    last_frame = None

    f = open("./output.mjpeg", "wb")
    write_buf_bytes(macroblock_size, 1, f)

    while (i := i + 1) and not (frame := vs.read()) is None:
        try:
            print("frame", f"{i:0>5}")
            last_frame = encode(frame, last_frame, f, i, macroblock_size)
            print()

            if i == 500:
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
        frames, rects = decode(fi, n=500)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(
        "out/normal.mp4", fourcc, float(10), (frames[0].shape[1], frames[0].shape[0])
    )

    for f in frames:
        video.write(f)

    video.release()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(
        "out/rect.mp4", fourcc, float(10), (rects[0].shape[1], rects[0].shape[0])
    )

    for f in rects:
        video.write(f)

    video.release()


if __name__ == "__main__":
    main()
