# Boletin-Oficial-Argentina
Código para la creación y actualización de un dataset conformado por la totalidad de la legislación nacional, accesible a través de https://www.argentina.gob.ar/normativa/

El JSON resultante (al día de 18/12/2023) tiene un tamaño de 1.57Gb

## Instalación
Instalamos BeautifulSoup para manipular el contenido HTML de la web

```
pip install bs4
```

Y luego clonamos el repositorio

```
git clone https://github.com/sandbox-ai/Boletin-Oficial-Argentina
cd Boletin-Oficial-Argentina
```

## Uso

### create()
Crea el dataset scrappeando toda la web

```python
from dataset_utils import create
from scrapper import Scrapper

dataset_file = 'Boletin_Oficial.jsonl' # Nombre del archivo de salida

scrapper = Scrapper()

create(scrapper, dataset_file)
```

### update()
Actualiza el dataset creado en el paso anterior
```python
from dataset_utils import update
from scrapper import Scrapper

dataset_file = 'Boletin_Oficial.jsonl' # Nombre del dataset a actualizar

scrapper = Scrapper()

update(scrapper, dataset_file)
```

## Formato de salida

El dataset producido es un JSONL con el siguiente formato:

```json
{
  "title":"Título resumido de la entrada",
  "name":"Nombre asignado",
  "entity":"Entidad gubernamental que la emite",
  "content":"Contenido de la entrada",
  "date":"Fecha publicada",
  "url":"url relativa"
}
```
