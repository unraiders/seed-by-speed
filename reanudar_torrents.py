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
client = Client(
    host=f'http://{QBITTORRENT_HOST}:{QBITTORRENT_PORT}',
    username=QBITTORRENT_USER,
    password=QBITTORRENT_PASSWORD,
)

def reanudar_torrents():
    logger.debug("Iniciando función reanudar_torrents()")
    
    # Verificar que el archivo existe
    if not os.path.exists('/app/data/torrents.txt'):
        logger.warning("El archivo torrents.txt no existe")
        return

    # Read the list of paused torrents
    try:
        with open('/app/data/torrents.txt', 'r') as f:
            torrents_to_resume = [line.strip() for line in f.readlines() if line.strip()]
        logger.debug(f"Leídos {len(torrents_to_resume)} torrents del archivo")
    except Exception as e:
        logger.error(f"Error leyendo torrents.txt: {str(e)}")
        return

    # List to keep track of torrents that were not resumed
    remaining_torrents = []

    try:
        # Obtener lista completa de torrents
        all_torrents = client.torrents_info()
        logger.debug(f"Total torrents en qBittorrent: {len(all_torrents)}")

        for torrent_name in torrents_to_resume:
            if not torrent_name:  # Skip empty lines
                continue
                
            logger.debug(f"Buscando torrent: {torrent_name}")
            # Buscar el torrent por nombre
            matching_torrents = [t for t in all_torrents if t.name == torrent_name]
            
            if matching_torrents:
                torrent = matching_torrents[0]  # Tomar el primer torrent que coincida
                client.torrents_resume(torrent.hash)
                logger.info(f"Reanudado torrent: {torrent_name}")
            else:
                logger.warning(f"No se encontró el torrent: {torrent_name}")
                remaining_torrents.append(torrent_name)
                
    except Exception as e:
        logger.error(f"Error procesando torrents: {str(e)}")
        # En caso de error, preservar la lista de torrents
        remaining_torrents = torrents_to_resume

    # Write back the remaining torrents
    try:
        with open('/app/data/torrents.txt', 'w') as f:
            for torrent_name in remaining_torrents:
                f.write(f"{torrent_name}\n")
        logger.debug(f"Guardados {len(remaining_torrents)} torrents pendientes")
    except Exception as e:
        logger.error(f"Error escribiendo torrents.txt: {str(e)}")

if __name__ == "__main__":
    logger.info("Iniciando script reanudar_torrents.py")
    reanudar_torrents()
    logger.info("Finalizado script reanudar_torrents.py")