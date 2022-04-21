import sys
from encoder import encode
from imutils.video import FileVideoStream


def main():
    # Main encoding loop while reading mp4
    vs = FileVideoStream("./Big_Buck_Bunny_1080_10s_10MB.mp4").start()
    i = 0

    f = open("./output.mjpeg", "wb")
    while (i := i + 1) and not (frame := vs.read()) is None:
        try:
            encode(frame, f)
        except:
            print(f"Could not read frame {i}", file=sys.stderr)
            return

    f.close()


if __name__ == "__main__":
    main()
