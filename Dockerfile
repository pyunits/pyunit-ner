FROM alpine:3.12.0
MAINTAINER Jytoui <jtyoui@qq.com>

EXPOSE 5000

ENV MODEL_PATH /mnt/model
RUN mkdir ${MODEL_PATH}

# 更换APK源
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装Python3环境
RUN apk add --no-cache --virtual mypacks \
            gcc  \
            python3-dev \
            py-pip \
            g++ \
            cmake \
            make \
            git && \
            apk add --no-cache python3

RUN ln /usr/bin/python3 /usr/bin/python

WORKDIR /opt

RUN wget http://oss.jtyoui.com/github/Paddle-1.8.3.tar.gz && \
    tar -zxvf Paddle-1.8.3.tar.gz && \
    rm -rf Paddle-1.8.3.tar.gz

RUN pip3 install --no-cache-dir numpy protobuf wheel

RUN mkdir build && \
    cd build && \
    cmake -S ../ -B . -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") && \
    make

ENV DIR /mnt/pyunit-ner
COPY ./ ${DIR}
WORKDIR ${DIR}

CMD ["sh","app.sh"]
