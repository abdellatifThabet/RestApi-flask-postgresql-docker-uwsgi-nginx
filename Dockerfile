FROM python:3.9-slim-buster

ENV FLASK_APP=app

WORKDIR /app/python-api

COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN apt-get -y install python3-dev build-essential libssl-dev libffi-dev python3-setuptools
Run pip install --upgrade pip


RUN pip install -r requirements.txt

COPY . ./

EXPOSE 5000


CMD ["uwsgi", "--ini", "uwsgi.ini"]



