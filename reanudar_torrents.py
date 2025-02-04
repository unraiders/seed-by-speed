import os
from utils import setup_logger
from qbit_config import get_qbittorrent_client

# Initialize logger
logger = setup_logger('reanudar_torrents')

def reanudar_torrents():
    logger.info("Iniciando proceso de reanudar torrents")
    
    # Get qBittorrent client
    client = get_qbittorrent_client()
    
    # Verificar que el archivo existe
    if not os.path.exists('/app/data/torrents.txt'):
        logger.warning("El archivo torrents.txt no existe")
        return

    # Leer la lista de torrents en pausa
    try:
        with open('/app/data/torrents.txt', 'r') as f:
            torrents_to_resume = [line.strip() for line in f.readlines() if line.strip()]
        logger.debug(f"Leídos {len(torrents_to_resume)} torrents del archivo")
    except Exception as e:
        logger.error(f"Error leyendo torrents.txt: {str(e)}")
        return

    # Lista para realizar un seguimiento de los torrents que no se reanudaron
    remaining_torrents = []

    try:
        # Obtener lista completa de torrents
        all_torrents = client.torrents_info()
        logger.debug(f"Total torrents en qBittorrent: {len(all_torrents)}")

        for torrent_name in torrents_to_resume:
            if not torrent_name:  
                continue
                
            logger.debug(f"Buscando torrent: {torrent_name}")
            # Buscar el torrent por nombre
            matching_torrents = [t for t in all_torrents if t.name == torrent_name]
            
            if matching_torrents:
                torrent = matching_torrents[0]  # Tomar el primer torrent que coincida
                client.torrents_resume(torrent.hash)
                logger.debug(f"Reanudado torrent: {torrent_name}")
            else:
                logger.warning(f"No se encontró el torrent: {torrent_name}")
                remaining_torrents.append(torrent_name)
                
    except Exception as e:
        logger.error(f"Error procesando torrents: {str(e)}")
        # En caso de error, preservar la lista de torrents
        remaining_torrents = torrents_to_resume

    # Escribe de nuevo los torrentes restantes
    try:
        with open('/app/data/torrents.txt', 'w') as f:
            for torrent_name in remaining_torrents:
                f.write(f"{torrent_name}\n")
        logger.debug(f"Guardados {len(remaining_torrents)} torrents pendientes")
    except Exception as e:
        logger.error(f"Error escribiendo torrents.txt: {str(e)}")

    logger.info("Finalizado proceso de reanudar torrents")

if __name__ == "__main__":
    reanudar_torrents()
