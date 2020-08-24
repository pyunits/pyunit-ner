FROM python:3.7-alpine
MAINTAINER Jytoui <jtyoui@qq.com>

# 加入pip源
ENV pypi=https://pypi.douban.com/simple \
    MODEL_PATH=/mnt/msra \
    DIR=/mnt/pyunit-ner

# 支持安装manylinux1编译的wheel包
#RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python3.7/site-packages/_manylinux.py
#RUN echo 'manylinux2014_compatible = True' > /usr/local/lib/python3.7/site-packages/_manylinux.py

# 开放端口
EXPOSE 5000

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --no-cache py3-six py3-requests curl unrar py3-numpy

# 构建编译环境
RUN apk add -U --no-cache --virtual=build_alpine_env \
    py-pip \
    gcc  \
    python3-dev \
    linux-headers \
    musl-dev && \
    pip install --no-cache-dir paddlepaddle flask uWSGI -i ${pypi} && \
    apk del build_alpine_env

#RUN curl -o /mnt/model.rar http://oss.jtyoui.com/model/实体抽取.rar && unrar x /mnt/model.rar && rm -rf /mnt/model.rar

COPY ./ ${DIR}
WORKDIR ${DIR}

CMD ["sh","app.sh"]
