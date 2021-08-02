FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER Jytoui <jtyoui@qq.com>
EXPOSE 80

COPY requirements.txt /app/requirements.txt
COPY ./pyunit_ner /app/pyunit_ner
COPY ./main.py /app/main.py

# 安装Python3环境
RUN wget -O /mnt/model.tar.gz https://github.com/PyUnit/pyunit-ner/releases/download/v1.0/model.tar.gz && \
    tar -zxvf /mnt/model.tar.gz  -C /mnt/ && \
    rm -rf /mnt/model.tar.gz && \
    pip3 install --no-cache-dir -r /app/requirements.txt  && \
    apt-get update && apt-get install -y libgl1-mesa-glx
