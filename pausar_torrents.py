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
# client = Client(host=QBITTORRENT_HOST, port=QBITTORRENT_PORT, username=QBITTORRENT_USER, password=QBITTORRENT_PASSWORD)

# Connect to qBittorrent
client = Client(
    host=f'http://{QBITTORRENT_HOST}:{QBITTORRENT_PORT}',
    username=QBITTORRENT_USER,
    password=QBITTORRENT_PASSWORD,
)

# Load trackers dictionary
with open('/app/data/trackers.dic', 'r') as f:
    trackers = json.load(f)
    logger.debug(f"Loaded trackers: {trackers}")

def pausar_torrents():
    logger.info("Iniciando proceso de pausado de torrents")
    
    for torrent in client.torrents_info():
        # Solo procesar si está en uploading
        # if not torrent.state_enum.is_uploading:
        if not torrent.state in ['uploading']:
            continue
            
        logger.debug(f"Procesando torrent en uploading: {torrent.name} (velocidad: {torrent.upspeed/1024:.2f} KB/s)")
        
        # Comprobar tiempo de seedeo
        current_time = time.time()
        seeding_time = (current_time - torrent.added_on) / 3600
        
        # Buscar tracker coincidente y activo
        matching_tracker = None
        for tracker_info in trackers:
            if tracker_info['activo'] == 'si' and tracker_info['Tracker'] in torrent.tracker:
                matching_tracker = tracker_info
                break
        
        if not matching_tracker:
            continue
            
        # Comprobar tiempo mínimo de seedeo
        if seeding_time <= matching_tracker['horas_sedeo_min']:
            continue
            
        logger.debug(f"- Cumple tiempo mínimo: {seeding_time:.2f}h > {matching_tracker['horas_sedeo_min']}h")
        
        # Comprobar velocidad mínima
        min_speed = matching_tracker['velocidad_min_kbps'] * 1024
        if torrent.upspeed < min_speed:
            logger.debug(f"- Velocidad por debajo del mínimo: {torrent.upspeed/1024:.2f} KB/s < {min_speed/1024:.2f} KB/s")
            try:
                client.torrents_pause(torrent.hash)
                with open('/app/data/torrents.txt', 'a') as f:
                    f.write(f"{torrent.name}\n")
                logger.info(f"Pausado torrent: {torrent.name}")
            except Exception as e:
                logger.error(f"Error al pausar torrent {torrent.name}: {str(e)}")

    logger.info("Proceso finalizado")

if __name__ == "__main__":
    logger.info("Iniciando script pausar_torrents.py")
    pausar_torrents()
    logger.info("Finalizado script pausar_torrents.py")