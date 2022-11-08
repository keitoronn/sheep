# ベースとなるイメージ
#FROM ubuntu:16.04
FROM python:3.7

# RUNでコンテナ生成時に実行する
RUN apt-get update
RUN apt-get install -y python3-pip python3-tk x11-apps 
RUN pip3 install --upgrade pip
COPY requirement.txt .
RUN pip3 install -r requirement.txt
#ENV DISPLAY host.docker.internal:0.0