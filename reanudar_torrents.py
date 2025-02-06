import os
from utils import setup_logger
from reanudar_qbittorrent import reanudar_torrents_qbittorrent
from reanudar_transmission import reanudar_torrents_transmission

# Initialize logger
logger = setup_logger('reanudar_torrents')
    
if __name__ == "__main__":
    torrent_client = os.getenv('TORRENT_CLIENT')

    if torrent_client == 'qbittorrent':
        reanudar_torrents_qbittorrent()
    elif torrent_client == 'transmission':
        reanudar_torrents_transmission()
    else:
        raise ValueError(f"Cliente de torrent no soportado: {torrent_client}")  