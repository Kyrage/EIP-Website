FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

ADD ./requirements.txt /code

RUN pip install --upgrade pip

RUN pip install -r /code/requirements.txt

ADD . /code/

EXPOSE 8080