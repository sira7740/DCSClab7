FROM ubuntu:20.04
FROM python:3.6-slim-stretch
RUN apt-get update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3 python3-pip python3-pillow python3-redis
RUN pip3 install git+https://github.com/ageitgey/face_recognition_models
RUN pip3 install pika
RUN pip3 install jsonpickle
RUN pip3 install pillow
RUN pip3 install redis
RUN pip3 install numpy
RUN mkdir /worker
WORKDIR /worker
copy . /worker
CMD python3 worker-server.py