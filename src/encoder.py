import cv2

from io import BufferedWriter
from numpy.typing import NDArray
from bitstring import BitArray

from util import write_buf


def jpeg(img: NDArray):
    is_success, contents = cv2.imencode(
        ext=".jpg", img=img, params=[cv2.IMWRITE_JPEG_QUALITY, 95]
    )

    if not is_success:
        raise "Failed JPEG writing"

    return contents, len(contents)


def encode(current_frame: NDArray, p_frame: NDArray, out: BufferedWriter) -> NDArray:
    if not p_frame:
        # Codec file Header
        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf(initial_frame_size, 2, out)
        write_buf(initial_frame, initial_frame_size, out)
        return current_frame

    for ii in range(0, current_frame.shape[0], 8):
        for jj in range(0, current_frame.shape[1], 8):
            print(ii, jj)

    
