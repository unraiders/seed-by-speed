import os
import time
from qbittorrentapi import Client
from utils import setup_logger

# Initialize logger
logger = setup_logger('qbit_config')

def get_qbittorrent_client(max_retries=float('inf'), retry_delay=5):
    # Load environment variables
    QBITTORRENT_HOST = os.getenv('QBITTORRENT_HOST')
    QBITTORRENT_PORT = os.getenv('QBITTORRENT_PORT')
    QBITTORRENT_USER = os.getenv('QBITTORRENT_USER')
    QBITTORRENT_PASSWORD = os.getenv('QBITTORRENT_PASSWORD')
    
    attempts = 0
    while attempts < max_retries:
        try:
            client = Client(
                host=f'http://{QBITTORRENT_HOST}:{QBITTORRENT_PORT}',
                username=QBITTORRENT_USER,
                password=QBITTORRENT_PASSWORD,
            )
            # Test connection
            client.auth_log_in()
            logger.info("Conectado a qBittorrent")
            return client
        except Exception as e:
            attempts += 1
            logger.error(f"Fallo al conectar a qBittorrent (intento {attempts}): {str(e)}")
            if attempts < max_retries:
                logger.info(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                raise Exception("Max reintentos. No se puede establecer conexión con qBittorrent")
