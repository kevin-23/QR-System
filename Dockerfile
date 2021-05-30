FROM python:3.8-buster
LABEL maintainer="kevin.23cabezas@gmail.com"

WORKDIR /app

COPY ./app/* /app/

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
       apt-get -y --quiet --no-install-recommends install  \
       libzbar0 \
       python3-tk \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && pip3 install -r requeriments.txt \
    && rm -rf ./requeriments.txt /var/lib/apt/lists/* /tmp/* /var/tmp/*
