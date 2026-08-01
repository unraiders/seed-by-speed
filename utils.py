import logging
import os
import re

from colorama import Fore, Style, init
from dotenv import load_dotenv

# Inicializar colorama
init(strip=False)  # Asegura que los códigos ANSI no se eliminen en macOS

# Cargar las variables del archivo .env
load_dotenv()

# Leer la variable DEBUG del archivo .env
DEBUG = os.getenv("DEBUG", "0") == "1"

# Definir colores para cada nivel de logging
COLORS = {
    logging.DEBUG: Fore.GREEN,
    logging.INFO: Fore.WHITE,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Aplicar color según el nivel del log
        color = COLORS.get(record.levelno, Fore.WHITE)
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# utils.py (actualización final)
def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = ColoredFormatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Control exhaustivo de librerías de terceros
    third_party_loggers = [
        'qbittorrentapi',
        'urllib3',
        'requests',
        'urllib3.connectionpool',
        'qbittorrentapi.decorators'
    ]

    for lib in third_party_loggers:
        lib_logger = logging.getLogger(lib)
        lib_logger.setLevel(logging.WARNING)
        lib_logger.propagate = False
        for handler in lib_logger.handlers[:]:
            lib_logger.removeHandler(handler)

    return logger


# Separador de campos en torrents.txt. Cada línea es "hash|nombre": el hash
# identifica el torrent y el nombre queda solo como referencia legible.
SEPARADOR_CAMPOS = "|"

# Un infohash es hexadecimal: 40 caracteres en v1 y 64 en v2.
_PATRON_HASH = re.compile(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}")


def formatear_linea_torrent(torrent_hash: str, nombre: str) -> str:
    """Construye la línea de torrents.txt para un torrent pausado."""
    # El nombre se limpia de espacios y saltos para que no rompa el formato.
    nombre_limpio = " ".join(nombre.split())
    return f"{torrent_hash}{SEPARADOR_CAMPOS}{nombre_limpio}\n"


def parsear_linea_torrent(linea: str):
    """Devuelve (hash, nombre) a partir de una línea de torrents.txt.

    Acepta el formato antiguo, que solo contenía el nombre del torrent, en cuyo
    caso el hash devuelto es None y hay que localizarlo por nombre.
    """
    linea = linea.strip()
    if not linea:
        return None, None

    posible_hash, separador, resto = linea.partition(SEPARADOR_CAMPOS)
    if separador and _PATRON_HASH.fullmatch(posible_hash.strip()):
        return posible_hash.strip().lower(), resto.strip()

    # Formato antiguo: la línea entera es el nombre del torrent.
    return None, linea

