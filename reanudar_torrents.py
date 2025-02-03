import os
from qbittorrentapi import Client
from utils import setup_logger

# Load environment variables
QBITTORRENT_HOST = os.getenv('QBITTORRENT_HOST')
QBITTORRENT_PORT = os.getenv('QBITTORRENT_PORT')
QBITTORRENT_USER = os.getenv('QBITTORRENT_USER')
QBITTORRENT_PASSWORD = os.getenv('QBITTORRENT_PASSWORD')
DEBUG = int(os.getenv('DEBUG', 0))

# Initialize logger
logger = setup_logger('reanudar_torrents')

# Connect to qBittorrent
client = Client(host=QBITTORRENT_HOST, port=QBITTORRENT_PORT, username=QBITTORRENT_USER, password=QBITTORRENT_PASSWORD)

def reanudar_torrents():
    with open('/app/data/torrents.txt', 'r') as f:
        torrents = f.readlines()
    for torrent_name in torrents:
        torrent_name = torrent_name.strip()
        torrent = client.torrents_info(torrent_name)
        if torrent:
            client.torrents_resume(torrent.hash)
            logger.debug(f"Resumed torrent: {torrent_name}")
    with open('/app/data/torrents.txt', 'w') as f:
        f.write("")

if __name__ == "__main__":
    reanudar_torrents()