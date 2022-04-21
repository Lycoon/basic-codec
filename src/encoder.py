from io import BufferedWriter
from numpy.typing import NDArray
import cv2


def encode(frame: NDArray, buffer: BufferedWriter):
    # contents is the jpeg frame in a byte buffer
    is_success, contents = cv2.imencode(
        ext=".jpg", img=frame, params=[cv2.IMWRITE_JPEG_QUALITY, 50]
    )

    if not is_success:
        raise

    # jpeg byte count header
    buffer.write((len(contents)).to_bytes(8, byteorder="big"))

    # jpeg content
    buffer.write(contents)
