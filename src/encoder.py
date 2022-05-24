import io
import itertools
import math
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


def abs_diff(A: NDArray, B: NDArray, max: int = 180):
    a = A - B
    b = np.uint8(A < B) * (max - 1) + 1
    return a * b


BLOCK_SIZE = 8

i = 0
ALL_BLOCKS = np.zeros(shape=(1, 1))
MAX_BLOCK_UPDATE = 10
ALL_BLOCKS_UPDATE = [[] for _ in range(MAX_BLOCK_UPDATE)]


def encode(
    current_frame: NDArray,
    p_frame: NDArray,
    out: BufferedWriter,
    i=None,
    macroblock=16,
) -> NDArray:
    BLOCK_SIZE = macroblock
    global ALL_BLOCKS
    global ALL_BLOCKS_UPDATE

    r1 = range(0, current_frame.shape[0], BLOCK_SIZE)
    r2 = range(0, current_frame.shape[1], BLOCK_SIZE)

    if p_frame is None:
        # Codec file Header
        write_buf_bytes(1, 1, out)
        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)

        dim = (current_frame.shape[0] + BLOCK_SIZE) * (
            current_frame.shape[1] + BLOCK_SIZE
        )
        ALL_BLOCKS = np.zeros(
            shape=(math.ceil(dim / BLOCK_SIZE**2), BLOCK_SIZE, BLOCK_SIZE, 3),
            dtype=np.uint8,
        )

        for ii, jj in itertools.product(r1, r2):
            ALL_BLOCKS_UPDATE[MAX_BLOCK_UPDATE - 1] = (ii, jj)

        print("using jpeg")
        return current_frame

    best_coords = []

    # grayscales the buffers
    block_current_HLS: NDArray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HLS).astype(
        np.uint8
    )
    block_p_frame_HLS: NDArray = cv2.cvtColor(p_frame, cv2.COLOR_BGR2HLS).astype(
        np.uint8
    )

    # absolute difference
    diff_h = abs_diff(block_current_HLS[:, :, 0], block_p_frame_HLS[:, :, 0], 180) / 180
    diff_l = abs_diff(block_current_HLS[:, :, 1], block_p_frame_HLS[:, :, 1], 255) / 255
    # diff_s = abs_diff(block_current_HLS[:, :, 2], block_p_frame_HLS[:, :, 2], 255) / 255

    # Loops over all blocks
    RATIO = 1 / 5
    if not i is None and i % 10 == 0:
        RATIO = 1 / 6

    block_idx = 0
    for ii, jj in itertools.product(r1, r2):
        for diff in [diff_h, diff_l]:
            block = diff[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
            sum_diff = np.sum(block)
            if sum_diff > BLOCK_SIZE**2 * RATIO or (ii, jj) in ALL_BLOCKS_UPDATE[0]:
                best_coords.append((ii, jj))
                block = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
                ALL_BLOCKS[
                    block_idx,
                    : block.shape[0],
                    : block.shape[1],
                    : block.shape[2],
                ] = block
                ALL_BLOCKS_UPDATE[MAX_BLOCK_UPDATE - 1] = (ii, jj)
                block_idx += 1
                break

    if block_idx > ALL_BLOCKS.shape[0] / 2:
        write_buf_bytes(1, 1, out)

        initial_frame, initial_frame_size = jpeg(current_frame)
        write_buf_bytes(initial_frame_size, 4, out)
        write_buf(initial_frame, out)

        print("using jpeg")
        return current_frame

    write_buf_bytes(0, 1, out)
    write_buf_bytes(len(best_coords), 2, out)
    for ii, jj in best_coords:
        write_buf_bytes(ii // BLOCK_SIZE, 2, out)
        write_buf_bytes(jj // BLOCK_SIZE, 2, out)
        block_curr = current_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE]
        p_frame[ii : ii + BLOCK_SIZE, jj : jj + BLOCK_SIZE] = block_curr

    print("blocks:", block_idx, "/", ALL_BLOCKS.shape[0])
    np.save(out, ALL_BLOCKS[:block_idx], allow_pickle=False)

    ALL_BLOCKS_UPDATE.pop(0)
    ALL_BLOCKS_UPDATE.append([])

    return p_frame
