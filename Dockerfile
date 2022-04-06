FROM python:3.8-slim-buster

WORKDIR /

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install libenchant-dev hunspell hunspell-es

COPY requirements.txt .
COPY app.py .
ADD templates templates

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT app:app
