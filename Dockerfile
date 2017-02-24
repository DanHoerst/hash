FROM python:2.7-alpine

MAINTAINER Dan Hoerst "dhoerst1@gmail.com"

ENV DB_USERNAME=admin
ENV DB_PASSWORD=default
ENV FLASK_APP=hash.py
ENV SITE_ADDRESS=localhost

RUN apk add --update openssl

COPY . /app
WORKDIR /app

RUN openssl genrsa -out /app/${SITE_ADDRESS}.key 2048
RUN openssl req -new -newkey rsa:4096 -key /app/${SITE_ADDRESS}.key \
    -out /app/${SITE_ADDRESS}.csr \
    -subj "/C=US/ST=New York/L=New York/O=Dis/CN=${SITE_ADDRESS}"
RUN openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost" \
    -keyout /app/${SITE_ADDRESS}.key  -out /app/${SITE_ADDRESS}.crt

RUN pip install -r requirements.txt
RUN flask initdb

CMD ["python", "hash.py"]
