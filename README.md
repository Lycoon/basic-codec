# CODEC (Motion-JPEG)

**DISCLAMER**: \
This is a dummy CODEC, this will not reduce your video, will greatly increase it's size. (~ x50)

## v0 architecture

```
        10 bits      |   frame_size bits
/---------------------------------------------\/---------------------------------------------\
| frame_size in bits |   JPEG Compression     || frame_size in bits |   JPEG Compression    | ...
\---------------------------------------------/\---------------------------------------------/
```

## v1 architecture

### Codec file header

```
8 bits  : Macroblock size
16 bits : Initial frame size
x bits  : JPEG initial frame (x being its size)
```

### Video data (per frame)

```
1 bit   : JPEG Flag

IF JPEG Flag = 1
16 bits : Frame size
x bits  : JPEG frame size

IF JPEG Flag = 0
16 bits : # of macroblocks

List OF macroblocks:
8 bits  : x coordinates
8 bits  : y coordinates
Macroblock size² * 3 : Macroblock to be refreshed

```

### Resources

[Motion-JPEG specifications](http://www.cajunbot.com/wiki/images/7/71/USB_Video_Payload_MJPEG_1.1.pdf)
