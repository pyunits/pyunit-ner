FROM daniobisous/alpine-opencv
MAINTAINER Jytoui <jtyoui@qq.com>

# 加入pip源
ENV pypi=https://pypi.douban.com/simple MODEL_PATH=/mnt/model DIR=/mnt/pyunit-ner

# 支持安装manylinux1编译的wheel包
RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python3.7/site-packages/_manylinux.py

# 开放端口
EXPOSE 5000

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories


#RUN pip install --no-cache-dir paddlepaddle==1.8.4 flask uWSGI -i ${pypi}
RUN pip install --no-cache-dir opencv-python -i ${pypi}

#RUN wget -P /home http://oss.jtyoui.com/model/实体抽取.rar

COPY ./ ${DIR}
WORKDIR ${DIR}

CMD ["sh","app.sh"]
