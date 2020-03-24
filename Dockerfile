FROM python:latest

RUN mkdir /WebApp
WORKDIR /WebApp
ADD ./WebApp /WebApp

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt