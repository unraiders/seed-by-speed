# seed-by-speed
Pausa/Reanuda torrents en qBittorrent basado en la velocidad de upload fuera de tiempo de sedeo.

### Instalación plantilla en Unraid.

- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-seed-by-speed.xml https://raw.githubusercontent.com/unraiders/seed-by-speed/refs/heads/main/my-seed-by-speed.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos seed-by-speed y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.

---
