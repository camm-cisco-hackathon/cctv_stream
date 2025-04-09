# rtsp_snapshot.py
import cv2

# RTSP URL 설정 (예: IP 카메라 주소)
RTSP_URL = "rtsp://192.168.128.11:9000/live"

# 저장할 파일명
SAVE_PATH = "snapshot.jpg"

# RTSP 스트림 열기
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("❌ RTSP 스트림을 열 수 없습니다.")
    exit()

# 프레임 한 장 캡처
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ 프레임 캡처 실패.")
    exit()

# 이미지 저장
cv2.imwrite(SAVE_PATH, frame)
print(f"✅ 이미지 저장 완료: {SAVE_PATH}")
