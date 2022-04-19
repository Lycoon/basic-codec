import numpy
from numpy.typing import NDArray
import imutils
from imutils.video import FileVideoStream


def main():
    # Main encoding loop while reading mp4
    vs = FileVideoStream("./Big_Buck_Bunny_1080_10s_10MB.mp4").start()
    while not (frame := vs.read()) is None:
        print(frame.shape)
        frame = imutils.resize(frame, width=400)


if __name__ == "__main__":
    main()
