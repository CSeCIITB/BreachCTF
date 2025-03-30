FROM ubuntu:24.04

RUN useradd -ms /bin/bash ctf

USER root
RUN apt-get -y update
RUN apt-get -y install socat build-essential

WORKDIR /home/ctf

COPY . .

RUN chown -R root:root /home/ctf
RUN chmod -R 755 /home/ctf

RUN chmod 755 main

USER ctf
EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork 'EXEC:./main'
