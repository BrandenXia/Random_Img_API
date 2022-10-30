FROM python:3

MAINTAINER SB, Peter, and Chara

RUN pip install random_img_api

EXPOSE 8045

VOLUME /img

CMD img_api run