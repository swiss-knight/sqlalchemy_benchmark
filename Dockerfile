FROM python:3.10.7-bullseye

COPY requirements.txt /

RUN python3 -m pip install -U pip \
  && python3 -m pip install -r requirements.txt

WORKDIR /app

