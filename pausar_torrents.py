import os
import time
import json
from qbittorrentapi import Client
from utils import setup_logger

# Load environment variables
QBITTORRENT_HOST = os.getenv('QBITTORRENT_HOST')
QBITTORRENT_PORT = os.getenv('QBITTORRENT_PORT')
QBITTORRENT_USER = os.getenv('QBITTORRENT_USER')
QBITTORRENT_PASSWORD = os.getenv('QBITTORRENT_PASSWORD')
DEBUG = int(os.getenv('DEBUG', 0))

# Initialize logger
logger = setup_logger('pausar_torrents')

# Connect to qBittorrent
client = Client(host=QBITTORRENT_HOST, port=QBITTORRENT_PORT, username=QBITTORRENT_USER, password=QBITTORRENT_PASSWORD)

# Load trackers dictionary
with open('/app/data/trackers.dic', 'r') as f:
    trackers = json.load(f)
    logger.debug(f"Loaded trackers: {trackers}")

def pausar_torrents():
    torrents = client.torrents_info()
    for torrent in torrents:
        if torrent.state == 'uploading':
            for tracker in trackers:
                if tracker['activo'] == 'si' and tracker['Tracker'] in torrent.tracker:
                    if time.time() - torrent.added_on > tracker['horas_sedeo_min'] * 3600:
                        if torrent.upspeed < tracker['velocidad_min_kbps'] * 1024:
                            client.torrents_pause(torrent.hash)
                            with open('/app/data/torrents.txt', 'a') as f:
                                f.write(f"{torrent.name}\n")
                            logger.debug(f"Paused torrent: {torrent.name}")

if __name__ == "__main__":
    pausar_torrents()