from io import BufferedWriter
import sys

import cv2
from encoder import encode
from decoder import decode

from imutils.video import FileVideoStream
from bitstring import BitArray


def write_buf(value: int, bytes: int, buf: BufferedWriter):
    buf.write(value.to_bytes(bytes, byteorder="big"))


def main():
    macroblock_size = 8

    # Main encoding loop while reading mp4
    vs = FileVideoStream("./Big_Buck_Bunny_1080_10s_10MB.mp4").start()

    i = 0
    last_frame = None

    f = open("./output.mjpeg", "wb")
    write_buf(macroblock_size, 1, f)

    while (i := i + 1) and not (frame := vs.read()) is None:
        try:
            last_frame = encode(frame, last_frame, f)
        except:
            print(f"Could not read frame {i}", file=sys.stderr)
            return

    f.close()

    with open("./output.mjpeg", "rb") as fi:
        frames = decode(fi, n=1)


if __name__ == "__main__":
    main()
