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

    for i in range(1, n):
        print(i)
        nb_pts = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
        points = []
        for _ in range(nb_pts):
            y = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
            x = int.from_bytes(read_exactly(buffer, 2), byteorder="big")
            points.append((y * block_size, x * block_size))

        buff_array_size = int.from_bytes(read_exactly(buffer, 8), byteorder="big")
        print(buff_array_size)
        buff_array = buffer.read(buff_array_size)

        data = np.frombuffer(buff_array, dtype=np.uint8)
        data = data.reshape((-1, block_size, block_size, 3))

        frame = np.copy(frame)
        for block_idx, pos in enumerate(points):
            ii = pos[0]
            jj = pos[1]
            block = data[block_idx]

            print("ii: ", ii, ", jj: ", jj)
            print("block_idx: ", block_idx)
            print("block_size: ", block_size, ", block.shape: ", block.shape)
            frame[ii : ii + block_size, jj : jj + block_size] = block

        out.append(frame)

    return out
