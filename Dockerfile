FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools
WORKDIR /src


RUN set -eux \
    && apk update && apk upgrade  \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    python3-dev \
    bash \
    git \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip \
    && rm -rf tmp


COPY . .

RUN pip install -r requirements.txt

EXPOSE ${SERVER_PORT}