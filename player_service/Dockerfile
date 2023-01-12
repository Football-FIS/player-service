# syntax=docker/dockerfile:1.4

FROM python:3.8-alpine AS builder
EXPOSE $PORT
WORKDIR /player_service
COPY requirements.txt /player_service
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /player_service
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app