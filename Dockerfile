FROM python:3

MAINTAINER SB, Peter, and Chara

COPY . /

RUN pip install -r requirements.txt

EXPOSE 8045

VOLUME /img

CMD gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8045 > ./logs/"$now".log 2>&1 &