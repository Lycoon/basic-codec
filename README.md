# CODEC (Motion-JPEG)

**DISCLAMER**: \
This is a dummy CODEC, this will not reduce your video, will greatly increase it's size. (~ x50)

## v0 architecture

### Codec file header

None

### Video data (per frame)

```
10 bits    : FRAME_BYTES
FRAME_BYTES: JPEG Compression
```

## v1 architecture

### Codec file header

| Bit/Byte | Data |
|-------|------|
| 8 bits  | Macroblock size |
| 32 bits | INIT_FRAME_BYTES |
| INIT_FRAME_BYTES | JPEG initial frame |

### Video data (per frame)


JPEG Flag is 1 (P-Frame)

| Bit/Byte | Data |
|-------|------|
| 8 bits  | Flags |
| 32 bits | INIT_FRAME_BYTES |
| INIT_FRAME_BYTES | JPEG initial frame |

JPEG Flag is 0 (I-Frame)

| Bit/Byte | Data |
|-------|------|
| 8 bits  | Flags |
| 8 bits  | X coord. |
| 8 bits  | Y coord. |
| MacroBlock**2 * 3 | Macroblock Refresh |

### Resources

[Motion-JPEG specifications](http://www.cajunbot.com/wiki/images/7/71/USB_Video_Payload_MJPEG_1.1.pdf)
