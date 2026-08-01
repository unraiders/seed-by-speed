# Cambios en esta versión

### v1.3.2

## 🐞 Correcciones

- Corregido el caso de torrents que se pausaban correctamente pero nunca se reanudaban, quedando en pausa de forma indefinida.

  El torrent se identificaba por su **nombre**, y al guardarlo se escribía tal cual mientras que al leerlo se le aplicaba `strip()`. Si el nombre tenía espacios al principio o al final, la comparación exacta ya nunca volvía a coincidir y el torrent se reintentaba en cada ejecución sin éxito.

  Ahora el torrent se identifica por su **hash**, que es único e inmutable.

## 🔧 Mejoras

- Nuevo formato de `torrents.txt`, con el carácter `|` como separador de campos:

  ```
  a94a8fe5ccb19ba61c4c0873d391e987982fbbd3|Nombre del torrent
  ```

  El hash es el que se usa para localizar y reanudar el torrent; el nombre se mantiene únicamente como referencia legible.

- El formato anterior (solo el nombre) se sigue leyendo, por lo que no es necesario migrar ni borrar el fichero `torrents.txt` existente. Las líneas antiguas se localizan por nombre, como hasta ahora, y se van reemplazando por el formato nuevo a medida que se pausan torrents.

- Al guardar el nombre se normalizan los espacios sobrantes, tabuladores y saltos de línea, de forma que no puedan romper el formato del fichero.

- Los mensajes de log de pausado y reanudado incluyen ahora el hash del torrent además del nombre.

> [!NOTE]
> Un torrent que ya estuviera atascado en `torrents.txt` con el formato antiguo seguirá sin reanudarse, porque su línea no contiene el hash. Para desatascarlo basta con borrar esa línea del fichero y reanudar el torrent manualmente; la próxima vez que se pause se registrará ya con el formato nuevo.
