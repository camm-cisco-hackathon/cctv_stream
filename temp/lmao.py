import cv2
import datetime

# RTSP 스트림 URL (Meraki 또는 기타 RTSP 지원 카메라)
RTSP_URL = "rtsp://192.168.128.11:9000/live"

# 저장할 파일 이름 설정 (날짜+시간 기반)
filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4"

# VideoCapture로 스트림 열기
cap = cv2.VideoCapture(RTSP_URL)

# 스트림이 열리지 않으면 종료
if not cap.isOpened():
    print("❌ RTSP 스트림을 열 수 없습니다.")
    exit()

# 프레임 너비, 높이, FPS 설정 (기본값 사용)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
fps = cap.get(cv2.CAP_PROP_FPS) or 15.0

# VideoWriter 설정 (코덱, 파일명, FPS, 해상도)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 또는 'XVID' for .avi
out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

print(f"📹 저장 시작: {filename}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❗ 스트림 수신 실패. 저장 종료.")
        break

    # 영상 저장
    out.write(frame)

    # (선택) 실시간 미리보기
    cv2.imshow('RTSP Stream', frame)

    # q 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 사용자에 의해 중단됨.")
        break

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()

print("✅ 저장 완료.")
