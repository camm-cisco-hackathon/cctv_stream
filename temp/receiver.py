# stream_server.py
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# 여기에 RTSP URL을 넣어줘 (예: 테스트용 IP 카메라)
RTSP_URL = "rtsp://192.168.128.11:9000/live"

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        raise RuntimeError("RTSP stream cannot be opened.")
    
    print(cap.isOpened())
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@app.get("/video")
def video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
