FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER Jytoui <jtyoui@qq.com>

COPY requirements.txt /app/requirements.txt

# 加入pip源
ENV pypi https://pypi.douban.com/simple

# 安装Python3环境
RUN pip3 install --no-cache-dir -r /app/requirements.txt -i ${pypi}

RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32

COPY ./sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y libgl1-mesa-glx
COPY ./pyunit_ner /app/pyunit_ner
COPY ./main.py /app/main.py
