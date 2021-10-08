FROM python:3.9-slim

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    python-dev
RUN apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /galangal
ADD . /galangal/
WORKDIR /galangal

RUN pip install -r requirements.txt

COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh
