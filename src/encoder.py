import io
import itertools
import os
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
ALL_BLOCKS = np.zeros(shape=(1, 1))


def encode(
    current_frame: NDArray,
    p_frame: NDArray,
    out: BufferedWriter,
    i=None,
    macroblock=16,
    latest_jpeg=0,
) -> NDArray:
    BLOCK_SIZE = macroblock
    global ALL_BLOCKS

    if p_frame is None:
        # Codec file Header
        write_buf_bytes(1, 1, out)
        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)

        dim = current_frame.shape[0] * current_frame.shape[1]
        ALL_BLOCKS = np.zeros(
            shape=(dim // BLOCK_SIZE**2, BLOCK_SIZE, BLOCK_SIZE, 3), dtype=np.uint8
        )

        print("using jpeg")
        return current_frame, True

    r1 = range(0, current_frame.shape[0], BLOCK_SIZE)
    r2 = range(0, current_frame.shape[1], BLOCK_SIZE)
    best_coords = []

    # grayscales the buffers
    block_current_gray: NDArray = np.sum(current_frame, axis=2).astype(np.uint8)
    block_p_frame_gray: NDArray = np.sum(p_frame, axis=2).astype(np.uint8)

    # absolute difference
    diff_gray = abs_diff(block_current_gray, block_p_frame_gray) / 255

    # Loops over all blocks
    RATIO = 1 / 5
    if not i is None and i % 10 == 0:
        RATIO = 1 / 6

    block_idx = 0
    for ii, jj in itertools.product(r1, r2):
        block = diff_gray[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        sum_diff = np.sum(block)
        if sum_diff > BLOCK_SIZE**2 * RATIO:
            best_coords.append((ii, jj))
            block = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
            ALL_BLOCKS[
                block_idx,
                : block.shape[0],
                : block.shape[1],
                : block.shape[2],
            ] = block
            block_idx += 1

    if i - latest_jpeg >= 10 and block_idx > ALL_BLOCKS.shape[0] / 8:
        write_buf_bytes(1, 1, out)

        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)

        dim = current_frame.shape[0] * current_frame.shape[1]
        ALL_BLOCKS = np.zeros(
            shape=(dim // BLOCK_SIZE**2, BLOCK_SIZE, BLOCK_SIZE, 3), dtype=np.uint8
        )

        print("using jpeg")
        return current_frame, True

    write_buf_bytes(0, 1, out)
    write_buf_bytes(len(best_coords), 2, out)
    for ii, jj in best_coords:
        write_buf_bytes(ii // BLOCK_SIZE, 2, out)
        write_buf_bytes(jj // BLOCK_SIZE, 2, out)
        block_curr = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        p_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE] = block_curr

    print("blocks:", block_idx, "/", ALL_BLOCKS.shape[0])
    np.save(out, ALL_BLOCKS[:block_idx], allow_pickle=False)
    return p_frame, False
