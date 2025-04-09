# app.py
import ffmpeg
import numpy as np
import cv2
import time
import os

width, height = 1920, 1080
rtsp_url = 'rtsp://192.168.128.11:9000/live'

output_dir = 'frames'
os.makedirs(output_dir, exist_ok=True)

process = (
    ffmpeg
    .input(rtsp_url, rtsp_transport='tcp')
    .output('pipe:', format='rawvideo', pix_fmt='bgr24', loglevel='quiet')
    .run_async(pipe_stdout=True)
)

print("[INFO] 스트리밍 시작. 0.5초마다 프레임 저장 중...")

saved_count = 0
last_saved_time = time.time()

while True:
    in_bytes = process.stdout.read(width * height * 3)
    if not in_bytes:
        break

    frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
    now = time.time()

    if now - last_saved_time >= 0.5:
        filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[저장] {filename}")
        last_saved_time = now
        saved_count += 1

    cv2.imshow('Meraki RTSP Stream (every 0.5s)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] 종료 키 입력됨")
        break

cv2.destroyAllWindows()
process.terminate()
print(f"[INFO] 저장 완료. 총 {saved_count}장의 프레임이 저장되었습니다.")
