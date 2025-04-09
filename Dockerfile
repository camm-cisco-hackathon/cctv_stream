# 베이스 이미지
FROM python:3.9-slim

# 필요한 패키지 설치 (ffmpeg 포함)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY app.py .

# frames 저장 폴더 생성
RUN mkdir -p frames

# 실행
CMD ["python", "app.py"]
