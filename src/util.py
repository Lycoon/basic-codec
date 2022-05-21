from io import BufferedWriter

def write_buf_bytes(value: int, bytes: int, buf: BufferedWriter):
    buf.write(value.to_bytes(bytes, byteorder="big"))

def write_buf(value, buf: BufferedWriter):
    buf.write(value)
