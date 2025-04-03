FROM python:3.9-slim

RUN useradd -ms /bin/bash ctf

RUN apt-get -y update && \
    apt-get -y install socat build-essential procps

WORKDIR /home/ctf

COPY . .

RUN chown -R root:root /home/ctf
RUN chmod -R 755 /home/ctf

RUN chmod 755 main.py

USER ctf

EXPOSE 12345

CMD ["socat", "TCP-LISTEN:12345,reuseaddr,fork", "EXEC:python3 main.py"]
