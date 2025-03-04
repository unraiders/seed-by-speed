# seed-by-speed

Pausa/Reanuda torrents en qBittorrent y Transmission basado en la velocidad de upload fuera de tiempo de sedeo.

Funcionamiento:

- :pause_button: Pausa los torrents en qBittorrent o Transmission si se dan todas estas circunstancias al ejecutarse el cron pausar:
	- :arrow_double_up: El estado del torrent es "uploading".
	- :date: Si la diferencia entre la fecha y hora actual es superior al valor de la clave horas_sedeo_min en el fichero trackers.dic.
	- :ok_hand: El valor de la clave Tracker corresponde y el valor de la clave activo es = si en el fichero trackers.dic.
	- :arrow_down: La velocidad actual del "upload" del torrent es inferior a la velocidad especificada en el valor de la clave velocidad_min_kbps en el fichero trackers.dic.
- :recycle: Reanuda los torrents en qBittorrent o Transmission pausados y que existen el fichero torrents.txt (generado por el programa) al ejecutarse el cron restaurar.

---
## Configuración variables de entorno y rutas.

| CLAVE                   | NECESARIO | VALOR                                                                                                                                     |
| :---------------------- | :-------: | :---------------------------------------------------------------------------------------------------------------------------------------- |
| TORRENT_CLIENT          |     ✅    | Cliente de descarga de Torrents. (qbittorrent o transmission)                                                                             |
| TORRENT_CLIENT_HOST     |     ✅    | Host/IP del cliente Torrent. Ejemplo: 192.168.2.20                                                                                        |
| TORRENT_CLIENT_PORT     |     ✅    | Puerto del cliente Torrent. Ejemplo: 8090                                                                                                 |
| TORRENT_CLIENT_USER     |     ✅    | Usuario del cliente Torrent.                                                                                                              |
| TORRENT_CLIENT_PASSWORD |     ✅    | Contraseña del cliente Torrent.                                                                                                           |
| CRON_PAUSAR             |     ✅    | Cron para pausar las descargas. (formato crontab. ej., */30 * * * * = cada 30 minutos, visita https://crontab.guru/ para más info.        |
| CRON_REANUDAR           |     ✅    | Cron para reanudar las descargas. (formato crontab. ej., 0 7 * * * = cada día a las 7:00 AM, visita https://crontab.guru/ para más info.) |
| DEBUG                   |     ✅    | Habilita el modo Debug en el log. (0 = No / 1 = Si)                                                                                       |
| TZ                      |     ✅    | Timezone (Por ejemplo: Europe/Madrid)                                                                                                     |

#### Volúmenes
Es necesario mapear tu carpeta local a /app/data para guardar los ficheros tracker.dic y el torrents.txt generado por el programa.

---

## Ejemplo docker-compose.yml
```yaml
services:
  seed-by-speed:
    image: unraiders/seed-by-speed
    container_name: seed-by-speed
    environment:
      - TORRENT_CLIENT=qbittorrent|transmission # dejar el deseado
      - TORRENT_CLIENT_HOST=192.168.2.20
      - TORRENT_CLIENT_PORT=8090
      - TORRENT_CLIENT_USER=admin
      - TORRENT_CLIENT_PASSWORD=adminadmin
      - CRON_PAUSAR=*/30 * * * * # formato crontab
      - CRON_REANUDAR=0 7 * * * # formato crontab
      - DEBUG=1
      - TZ=Europe/Madrid
    volumes:
      - /tu/ruta/local/seed-by-speed/:/app/data
    entrypoint: ./entrypoint.sh
```

---
### Instalación plantilla en Unraid.

- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-seed-by-speed.xml https://raw.githubusercontent.com/unraiders/seed-by-speed/refs/heads/main/my-seed-by-speed.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos seed-by-speed y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.

---

  > [!IMPORTANT]
  > Se tiene que descargar del repositorio el fichero trackers_EJEMPLO.dic, renombrarlo a trackers.dic, rellenar el valor de las claves Tracker según nuestras necesidades y colocar el fichero en la carpeta local mapeada anteriormente

---

  > [!TIP]
  > Activando la variable DEBUG = 1 podemos tener un log detallado de los torrents que pausará/reanudará en el cliente de torrents y algunos detalles adicionales.

---

Fin.
