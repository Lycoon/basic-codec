import cv2

from io import BufferedWriter
from msilib.schema import Error
from numpy.typing import NDArray
from bitstring import BitArray

from main import write_buf


def write_jpeg(img: NDArray):
    is_success, contents = cv2.imencode(
        ext=".jpg", img=img, params=[cv2.IMWRITE_JPEG_QUALITY, 95]
    )

    if not is_success:
        raise Error("Failed JPEG writing")

    return contents, len(contents)


def encode(current_frame: NDArray, p_frame: NDArray, out: BufferedWriter) -> NDArray:
    if not p_frame:
        initial_frame, initial_frame_size = write_jpeg(current_frame)
        write_buf(initial_frame_size, 2, out)
