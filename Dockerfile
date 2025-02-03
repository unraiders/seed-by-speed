FROM python:3.12-alpine

LABEL maintainer="unraiders"
LABEL description=""

ARG VERSION=1.0.0
ENV VERSION=${VERSION}

RUN apk add --no-cache dcron mc

WORKDIR /app

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pausar_torrents.py .
COPY reanudar_torrents.py .

COPY utils.py .

ENTRYPOINT ["./entrypoint.sh"]