import itertools
import cv2

from io import BufferedWriter
from numpy.typing import NDArray
from bitstring import BitArray
import numpy as np
from scipy import spatial

from util import write_buf, write_buf_bytes


def jpeg(img: NDArray):
    is_success, contents = cv2.imencode(
        ext=".jpg", img=img, params=[cv2.IMWRITE_JPEG_QUALITY, 95]
    )

    if not is_success:
        raise "Failed JPEG writing"

    return contents, len(contents)


def abs_diff(A: NDArray, B: NDArray):
    a = A - B
    b = np.uint8(A < B) * 254 + 1
    return a * b


BLOCK_SIZE = 8


def encode(current_frame: NDArray, p_frame: NDArray, out: BufferedWriter) -> NDArray:
    if p_frame is None:
        # Codec file Header
        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)
        return current_frame

    r1 = range(0, current_frame.shape[0], BLOCK_SIZE)
    r2 = range(0, current_frame.shape[1], BLOCK_SIZE)
    count = 0
    # Loops over all blocks
    for ii, jj in itertools.product(r1, r2):
        block_current = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        block_p_frame = p_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]

        # grayscales the buffers
        block_current: NDArray = np.sum(block_current, axis=2).astype(np.uint8)
        block_p_frame: NDArray = np.sum(block_p_frame, axis=2).astype(np.uint8)

        # absolute difference
        diff = abs_diff(block_current, block_p_frame) / 255
        print(diff[:4, :4])
        sum_diff = np.sum(diff)
        if sum_diff < 16:
            count += 1

    # TODO: return the actual frame
    return current_frame


# if block_current.shape != (8, 8, 3):
# tmp = np.zeros(shape=(8, 8, 3), dtype=np.uint8)
# tmp[: block_current.shape[0], : block_current.shape[1]] = block_current
# block_current = tmp
