FROM python:3.12-alpine

LABEL maintainer="unraiders"
LABEL description="Pausa/Reanuda torrents en qBittorrent o Transmission basado en la velocidad de upload fuera de tiempo de sedeo obligatorio."

ARG VERSION=1.1.1
ENV VERSION=${VERSION}

RUN apk add --no-cache dcron mc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pausar_torrents.py .
COPY reanudar_torrents.py .

COPY pausar_qbittorrent.py .
COPY reanudar_qbittorrent.py .

COPY pausar_transmission.py .
COPY reanudar_transmission.py .

COPY cliente_torrent_config.py .

COPY utils.py .

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]