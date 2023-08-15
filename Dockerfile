FROM python:3.8.15-slim-buster

COPY requirements.txt .
COPY yolov5/requirements.txt ./yolo_requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && pip install -r yolo_requirements.txt --no-cache-dir

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
