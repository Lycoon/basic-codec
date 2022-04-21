from io import BufferedReader
from numpy.typing import NDArray
import cv2


def decode(buffer: BufferedReader, n=1):
    out = []

    if n <= 0:
        return []

    for _ in range(0, n):
        nb_bytes = buffer.read(8)
        nb_bytes = int.from_bytes(nb_bytes, byteorder="big")

        bytes_buffer = buffer.read(nb_bytes)

        out.append(bytes_buffer)

    return out
