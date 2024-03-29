FROM python:2.7-alpine
MAINTAINER DCU ENG <DCUEng@godaddy.com>


RUN addgroup -S dcu && adduser -H -S -G dcu dcu
RUN apk update && \ 
    apk add --no-cache build-base \
    unixodbc-dev \
    freetds-dev

COPY ./run.py ./settings.py ./logging.yaml /app/
COPY . /tmp/

RUN chown -R dcu:dcu /app

RUN pip install --compile /tmp && rm -rf /tmp/*
WORKDIR /app

RUN echo -en "[FreeTDS]\n\
Description=FreeTDS unixODBC Driver\n\
Driver=/usr/lib/libtdsodbc.so\n" > /etc/odbcinst.ini

ENTRYPOINT ["python", "/app/run.py"]