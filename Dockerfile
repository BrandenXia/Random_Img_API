FROM python:3

MAINTAINER SB, Peter, and Chara

COPY . /

RUN pip install -r requirements.txt

EXPOSE 8080

VOLUME /img

CMD uvicorn main:app --port 8000