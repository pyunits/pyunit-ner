FROM python:3.7
MAINTAINER Jytoui <jtyoui@qq.com>

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 425956BB3E31DF51
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install unrar -y
RUN wget -P /home http://oss.jtyoui.com/model/实体抽取.rar

ENV MODEL_PATH /mnt/model
RUN mkdir ${MODEL_PATH}

ENV DIR /mnt/pyunit-ner
COPY ./ ${DIR}
WORKDIR ${DIR}

RUN unrar e /home/实体抽取.rar ${MODEL_PATH} && rm -rf /home/实体抽取.rar
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh","app.sh"]
