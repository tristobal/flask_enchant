FROM python:3.8-slim-buster

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install libenchant-dev hunspell hunspell-es

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
