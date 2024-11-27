# Boletin-Oficial-Argentina
Código para la creación y actualización de un dataset conformado por la totalidad de la legislación nacional, accesible a través de https://www.argentina.gob.ar/normativa/


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
  "summary":"Resumen de la entrada",
  "full_text":"Contenido completo",
  "url_in_articles":"URLs encontradas en la entrada",
  "date":"Fecha publicada",
  "url":"url relativa"
}
```

## [Dataset en Huggingface🤗](https://huggingface.co/datasets/marianbasti/boletin-oficial-argentina)
Actualizada diariamente

Estado de la última actualizacion: 
[![Update HuggingFace Dataset](https://github.com/sandbox-ai/Boletin-Oficial-Argentina/actions/workflows/update_hf_dataset.yml/badge.svg)](https://github.com/sandbox-ai/Boletin-Oficial-Argentina/actions/workflows/update_hf_dataset.yml)
