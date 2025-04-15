FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install flask gunicorn

RUN pip install flask
EXPOSE 8080

CMD ["gunicorn", "-w", "8", "-t", "5", "--graceful-timeout", "0", "-b", "0.0.0.0:8080", "server:app"]
