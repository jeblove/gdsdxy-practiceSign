FROM python:3.6

MAINTAINER jeblove 249972068@qq.com

ADD ./practiceSignFunc.tar.gz /code
ADD ./requirements.txt /code

WORKDIR /code

RUN python -m pip install --upgrade pip
RUN pip config set global.index-url https://repo.huaweicloud.com/repository/pypi/simple
RUN pip install -r requirements.txt -i https://repo.huaweicloud.com/repository/pypi/simple

ENV username username
ENV password password
ENV pushkey pushkey

CMD ["python", "/code/practiceSignFunc/index.py"]