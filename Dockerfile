FROM python:3.7-alpine
MAINTAINER Will Storer <william@birchbox.com>

ENV SERVICE_NAME ring-doorbell

RUN pip install ring_doorbell

RUN mkdir /app /log /conf
COPY src/ring-doorbell/ /app/

ENTRYPOINT ["python", "/app/ring-slack.py"]
