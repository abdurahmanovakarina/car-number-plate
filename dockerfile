FROM ubuntu:22.04

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    libx11-dev \
    libxext-dev \
    libxtst-dev && \
    rm -rf /var/lib/apt/lists/*
RUN apt update && apt upgrade -y 
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.10 python3.10-venv python3.10-dev
RUN apt install -y python3-pip
RUN apt install --fix-missing -y g++ ffmpeg libsm6 libxext6

RUN pip3 install --no-cache-dir "ultralytics==8.1.25"
RUN apt install libxcb-xinerama0 libqt5x11extras5 -y
RUN apt-get install libxcb-xinerama0 -y
RUN export QT_DEBUG_PLUGINS=1
RUN pip3 uninstall opencv-python -y
RUN pip3 install opencv-python-headless
RUN apt install python3-pyqt5 -y

COPY . /app/
CMD ["python3", "./main.py"]