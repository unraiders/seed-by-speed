import os

from cliente_torrent_config import get_transmission_client
from utils import formatear_linea_torrent, parsear_linea_torrent, setup_logger

# Initialize logger
logger = setup_logger('reanudar_transmission')

def reanudar_torrents_transmission():
    logger.info("Iniciando proceso de reanudar torrents")

    # Get torrent client
    client = get_transmission_client()

    # Verificar que el archivo existe
    if not os.path.exists('/app/data/torrents.txt'):
        logger.warning("El archivo torrents.txt no existe")
        return

    # Leer la lista de torrents en pausa
    try:
        with open('/app/data/torrents.txt', 'r') as f:
            torrents_to_resume = [parsear_linea_torrent(line) for line in f.readlines() if line.strip()]
        logger.debug(f"Leídos {len(torrents_to_resume)} torrents del archivo")
    except Exception as e:
        logger.error(f"Error leyendo torrents.txt: {str(e)}")
        return

    # Lista para realizar un seguimiento de los torrents que no se reanudaron
    remaining_torrents = []

    try:
        # Obtener lista completa de torrents
        all_torrents = client.get_torrents()
        logger.debug(f"Total torrents en cliente torrent: {len(all_torrents)}")

        # Índice por hash, que es el identificador fiable del torrent
        torrents_por_hash = {t.hashString.lower(): t for t in all_torrents}

        for torrent_hash, torrent_name in torrents_to_resume:
            if not torrent_hash and not torrent_name:
                continue

            logger.debug(f"Buscando torrent: {torrent_name} ({torrent_hash or 'sin hash'})")

            if torrent_hash:
                torrent = torrents_por_hash.get(torrent_hash)
            else:
                # Formato antiguo sin hash: última búsqueda posible, por nombre
                torrent = next((t for t in all_torrents if t.name == torrent_name), None)

            if torrent:
                client.start_torrent(torrent.hashString)
                logger.debug(f"Reanudado torrent: {torrent.name} ({torrent.hashString})")
            else:
                logger.warning(f"No se encontró el torrent: {torrent_name} ({torrent_hash or 'sin hash'})")
                remaining_torrents.append((torrent_hash, torrent_name))

    except Exception as e:
        logger.error(f"Error procesando torrents: {str(e)}")
        # En caso de error, preservar la lista de torrents
        remaining_torrents = torrents_to_resume

    # Escribe de nuevo los torrentes restantes
    try:
        with open('/app/data/torrents.txt', 'w') as f:
            for torrent_hash, torrent_name in remaining_torrents:
                if torrent_hash:
                    f.write(formatear_linea_torrent(torrent_hash, torrent_name))
                else:
                    f.write(f"{torrent_name}\n")
        logger.debug(f"Guardados {len(remaining_torrents)} torrents pendientes")
    except Exception as e:
        logger.error(f"Error escribiendo torrents.txt: {str(e)}")

    logger.info("Finalizado proceso de reanudar torrents")

if __name__ == "__main__":
    reanudar_torrents_transmission()
