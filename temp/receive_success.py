import ffmpeg
import numpy as np
import cv2

width, height = 1920, 1080  # ← 여기 실제 해상도 입력
rtsp_url = 'rtsp://192.168.128.11:9000/live'

process = (
    ffmpeg
    .input(rtsp_url, rtsp_transport='tcp')
    .output('pipe:', format='rawvideo', pix_fmt='bgr24', loglevel='quiet')
    .run_async(pipe_stdout=True)
)

while True:
    in_bytes = process.stdout.read(width * height * 3)
    if not in_bytes:
        break
    frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
    cv2.imshow('Meraki RTSP via ffmpeg-python', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
