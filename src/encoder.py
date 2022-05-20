import io
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

i = 0


def encode(
    current_frame: NDArray, p_frame: NDArray, out: BufferedWriter, i=None, macroblock=16
) -> NDArray:
    BLOCK_SIZE = macroblock
    if p_frame is None:
        # Codec file Header
        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(1, 1, out)  # flag
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)
        return current_frame

    r1 = range(0, current_frame.shape[0], BLOCK_SIZE)
    r2 = range(0, current_frame.shape[1], BLOCK_SIZE)
    best_coords = []

    # grayscales the buffers
    block_current_gray: NDArray = np.sum(current_frame, axis=2).astype(np.uint8)
    block_p_frame_gray: NDArray = np.sum(p_frame, axis=2).astype(np.uint8)

    # absolute difference
    diff_gray = abs_diff(block_current_gray, block_p_frame_gray) / 255

    f = open("tmp.blocks", "wb")

    # Loops over all blocks
    RATIO = 1 / 5
    if not i is None and i % 10 == 0:
        RATIO = 1 / 6

    for ii, jj in itertools.product(r1, r2):
        block = diff_gray[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        sum_diff = np.sum(block)
        if sum_diff > BLOCK_SIZE**2 * RATIO:
            best_coords.append((ii, jj))
            block = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
            np.save(f, block)

    f.close()

    rect = np.copy(p_frame)
    for ii, jj in best_coords:
        write_buf_bytes(ii // BLOCK_SIZE, 2, out)
        write_buf_bytes(jj // BLOCK_SIZE, 2, out)
        block = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        p_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE] = block
        np.save(out, block)
        cv2.rectangle(
            rect,
            (jj, ii),
            (jj + BLOCK_SIZE, ii + BLOCK_SIZE),
            [255, 0, 255],
        )

    cv2.imwrite(f"out/p_frame_{i:0>5}.jpeg", p_frame)
    cv2.imwrite(f"out/p_frame_blocks_{i:0>5}.jpeg", rect)

    return p_frame
