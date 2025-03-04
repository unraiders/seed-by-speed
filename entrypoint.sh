#!/bin/sh

# Validar formato cron
validar_cron() {
    if ! echo "$1" | grep -qE '^[*/0-9,-]+ [*/0-9,-]+ [*/0-9,-]+ [*/0-9,-]+ [*/0-9,-]+$'; then
        echo "Error: Formato cron inválido: $1"
        echo "Debe tener 5 campos: minuto hora día-mes mes día-semana"
        exit 1
    fi
}

# Validar el cliente torrent
validar_cliente_torrent() {
    if [[ "$1" != "qbittorrent" && "$1" != "transmission" ]]; then
        echo "Error: Cliente de torrent inválido: $1"
        echo "Debe ser 'qbittorrent' o 'transmission'"
        exit 1
    fi
}
validar_cliente_torrent "$TORRENT_CLIENT"

# Validar que HORA esté definida
if [ -z "$CRON_PAUSAR" ]; then
    echo "La variable CRON_PAUSAR no está definida."
    exit 1
fi
validar_cron "$CRON_PAUSAR"

if [ -z "$CRON_REANUDAR" ]; then
    echo "La variable CRON_REANUDAR no está definida."
    exit 1
fi
validar_cron "$CRON_REANUDAR"

# Confirmación de configuración de cron
echo "$(date +'%d-%m-%Y %H:%M:%S') $VERSION - Arrancando entrypoint.sh"
echo "$(date +'%d-%m-%Y %H:%M:%S') Cliente Torrent: $TORRENT_CLIENT"
echo "$(date +'%d-%m-%Y %H:%M:%S') Programación CRON_PAUSAR: $CRON_PAUSAR"
echo "$(date +'%d-%m-%Y %H:%M:%S') Programación CRON_REANUDAR: $CRON_REANUDAR"
echo "$(date +'%d-%m-%Y %H:%M:%S') Zona horaria: $TZ"
echo "$(date +'%d-%m-%Y %H:%M:%S') Debug: $DEBUG"

# Crear una línea para cada crontab
CRON_JOB_PAUSAR="$CRON_PAUSAR python3 /app/pausar_torrents.py >> /proc/1/fd/1 2>> /proc/1/fd/2"
CRON_JOB_REANUDAR="$CRON_REANUDAR python3 /app/reanudar_torrents.py >> /proc/1/fd/1 2>> /proc/1/fd/2"

# Agregar los trabajos al crontab
echo "$CRON_JOB_PAUSAR" > /etc/crontabs/root
echo "$CRON_JOB_REANUDAR" >> /etc/crontabs/root

# Iniciar cron en segundo plano
echo "Arrancando cron..."
crond -f -l 2 || { echo "Error arrancando cron"; exit 1; }