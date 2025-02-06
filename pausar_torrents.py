import os
from utils import setup_logger
from pausar_qbittorrent import pausar_torrents_qbittorrent
from pausar_transmission import pausar_torrents_transmission

# Initialize logger
logger = setup_logger('pausar_torrents')
    
if __name__ == "__main__":
    torrent_client = os.getenv('TORRENT_CLIENT')

    if torrent_client == 'qbittorrent':
        pausar_torrents_qbittorrent()
    elif torrent_client == 'transmission':
        pausar_torrents_transmission()
    else:
        raise ValueError(f"Cliente de torrent no soportado: {torrent_client}")  