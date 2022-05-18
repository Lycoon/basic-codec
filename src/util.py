from io import BufferedWriter

def write_buf(value: int, bytes: int, buf: BufferedWriter):
    buf.write(value.to_bytes(bytes, byteorder="big"))
