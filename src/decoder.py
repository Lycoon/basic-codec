import enum
from io import BufferedReader
import os
from numpy.typing import NDArray
import cv2
import numpy as np


def read_exactly(fd, size):
    data = b""
    remaining = size

    while remaining > 0:
        newdata = fd.read(remaining)
        if len(newdata) == 0:
            raise IOError("Failed to read enough data")
        data += newdata
        remaining -= len(newdata)

    return data


def decode(buffer: BufferedReader, n=1):
    out = []

    if n <= 0:
        return []

    block_size = int.from_bytes(read_exactly(buffer, 1), byteorder="big")

    nb_bytes = int.from_bytes(read_exactly(buffer, 4), byteorder="big")

    initial_frame = read_exactly(buffer, nb_bytes)
    initial_frame = np.fromstring(initial_frame, dtype=np.uint8)
    initial_frame = cv2.imdecode(initial_frame, cv2.IMREAD_UNCHANGED)

    out.append(initial_frame)

    frame = initial_frame

    for _ in range(1, n):
        nb_pts = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
        points = []
        for _ in range(nb_pts):
            y = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
            x = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
            points.append((y * block_size, x * block_size))

        data = np.load(buffer)

        frame = np.copy(frame)
        frameY, frameX = frame.shape[0], frame.shape[1]
        for block_idx, pos in enumerate(points):
            ii = pos[0]
            jj = pos[1]
            block = data[block_idx]

            ii_plus = min(block_size, frameY - ii)
            jj_plus = min(block_size, frameX - jj)

            frame[ii : ii + ii_plus, jj : jj + jj_plus] = block[:ii_plus, :jj_plus]

        out.append(frame)

    return out
