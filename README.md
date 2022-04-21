# CODEC (Motion-JPEG)

**DISCLAMER**: \
This is a dummy CODEC, this will not reduce your video, will greatly increase it's size. (~ x50)

## Current architecture

```
        10 bytes      |   frame_size bytes
/---------------------------------------------\/---------------------------------------------\
| frame_size in bytes |   JPEG Compression    || frame_size in bytes |   JPEG Compression    | ...
\---------------------------------------------/\---------------------------------------------/
```

### Resources

[Motion-JPEG specifications](http://www.cajunbot.com/wiki/images/7/71/USB_Video_Payload_MJPEG_1.1.pdf)
