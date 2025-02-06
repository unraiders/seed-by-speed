import os
import time
import json
from utils import setup_logger
from cliente_torrent_config import get_transmission_client

# Initialize logger
logger = setup_logger('pausar_transmission')

def pausar_torrents_transmission():
    logger.info("Iniciando proceso de pausado de torrents")
    
    # Get transmission client
    client = get_transmission_client()
    
    # Load trackers dictionary
    with open('/app/data/trackers.dic', 'r') as f:
        trackers = json.load(f)
        logger.debug(f"Loaded trackers: {trackers}")

    for torrent in client.get_torrents():
        # Solo procesar si está en seeding y subiendo
        if not (torrent.status in ['seeding'] and torrent.rate_upload > 0):
            continue
            
        logger.debug(f"Procesando torrent en uploading: {torrent.name} (velocidad: {torrent.rate_upload / 1024:.2f} KB/s)")
        
        # Comprobar tiempo de seedeo
        current_time = time.time()
        seeding_time = (current_time - torrent.added_date.timestamp()) / 3600
        
        # Buscar tracker coincidente y activo
        matching_tracker = None
        for tracker_info in trackers:
            if tracker_info['activo'] == 'si' and tracker_info['Tracker'] in torrent.trackers[0].fields['sitename']:
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
        if torrent.rate_upload < min_speed:
            logger.debug(f"- Velocidad por debajo del mínimo: {torrent.rate_upload/1024:.2f} KB/s < {min_speed/1024:.2f} KB/s")
            try:
                client.stop_torrent(torrent.hashString)
                with open('/app/data/torrents.txt', 'a') as f:
                    f.write(f"{torrent.name}\n")
                logger.info(f"Pausado torrent: {torrent.name}")
            except Exception as e:
                logger.error(f"Error al pausar torrent {torrent.name}: {str(e)}")
                
    logger.info("Finalizado proceso de pausado de torrents")
    
if __name__ == "__main__":
    pausar_torrents_transmission()