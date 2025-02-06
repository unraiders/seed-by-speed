import os
import time
from qbittorrentapi import Client as qbClient
from transmission_rpc import Client as transClient
from utils import setup_logger

# Initialize logger
logger = setup_logger('cliente_torrent_config')

def get_qbittorrent_client(max_retries=float('inf'), retry_delay=5):
    # Load environment variables
    TORRENT_CLIENT_HOST = os.getenv('TORRENT_CLIENT_HOST')
    TORRENT_CLIENT_PORT = os.getenv('TORRENT_CLIENT_PORT')
    TORRENT_CLIENT_USER = os.getenv('TORRENT_CLIENT_USER')
    TORRENT_CLIENT_PASSWORD = os.getenv('TORRENT_CLIENT_PASSWORD')
    
    attempts = 0
    while attempts < max_retries:
        try:
            client = qbClient(
                host=f'http://{TORRENT_CLIENT_HOST}:{TORRENT_CLIENT_PORT}',
                username=TORRENT_CLIENT_USER,
                password=TORRENT_CLIENT_PASSWORD,
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


def get_transmission_client(max_retries=float('inf'), retry_delay=5):
    # Load environment variables       
    TORRENT_CLIENT_HOST = os.getenv('TORRENT_CLIENT_HOST')
    TORRENT_CLIENT_PORT = os.getenv('TORRENT_CLIENT_PORT')
    TORRENT_CLIENT_USER = os.getenv('TORRENT_CLIENT_USER')
    TORRENT_CLIENT_PASSWORD = os.getenv('TORRENT_CLIENT_PASSWORD')

    attempts = 0
    while attempts < max_retries:
        try:
            # Initialize Transmission client
            client = transClient(
                host=TORRENT_CLIENT_HOST,
                port=TORRENT_CLIENT_PORT,
                username=TORRENT_CLIENT_USER,
                password=TORRENT_CLIENT_PASSWORD,
            )
            logger.info("Conectado a Transmission")
            return client
        except Exception as e:
            attempts += 1
            logger.error(f"Fallo al conectar a Transmission (intento {attempts}): {str(e)}")
            if attempts < max_retries:
                logger.info(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                raise Exception("Max reintentos. No se puede establecer conexión con Transmission")