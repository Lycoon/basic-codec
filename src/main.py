import sys
from imutils.video import FileVideoStream
import cv2


def main():
    # Main encoding loop while reading mp4
    vs = FileVideoStream("./Big_Buck_Bunny_1080_10s_10MB.mp4").start()
    i = 0
    while (i := i + 1) and not (frame := vs.read()) is None:
        # contents is the jpeg frame in a byte buffer
        is_success, contents = cv2.imencode(ext=".jpg", img=frame)
        if not is_success:
            print(f"Could not read frame {i}", file=sys.stderr)
            continue


if __name__ == "__main__":
    main()
