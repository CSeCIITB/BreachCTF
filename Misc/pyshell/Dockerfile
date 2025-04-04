FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt upgrade -y
RUN apt install socat -y
RUN mkdir /chall
RUN pip install --upgrade pip

COPY shell.py /chall
WORKDIR /chall

EXPOSE 1340
CMD socat TCP-LISTEN:1340,reuseaddr,fork EXEC:"python shell.py"
