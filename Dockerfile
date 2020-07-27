FROM python:3.7.4-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y cron nginx curl socat openssl tar tzdata gcc
COPY requirements.txt /code/
RUN pip install -r requirements.txt
