FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt upgrade -y
RUN apt install socat -y
RUN mkdir /chall
RUN pip install --upgrade pip
RUN pip3 install pycryptodome

COPY secret.py /chall/
COPY source.py /chall/
WORKDIR /chall

EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python source.py"
