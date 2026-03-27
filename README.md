# Museo del Prado – Artwork Scraper

Web scraper para el catálogo público del Museo del Prado. 

Extrae metadatos estructurados de todas las obras y los guarda en CSV.

------

## Prerequisitos

- Python 3.11+
- Google chromium instalado
- Playwright instalado y con los navegadores descargados (Ejecutar `playwright install chromium` tras las instalacion del paquete con PIP)

------

## Instalación y configuración

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar (Linux / macOS)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar los navegadores de Playwright (solo la primera vez)
playwright install chromium
```

------

## Ejecución

```bash
python main.py
```

El script abre un navegador Chromium visible, acepta las cookies del portal y arranca el proceso de scraping automáticamente.

------

## Fases de ejecución

El scraper trabaja en dos fases:

**Fase 1 – Recolección de links** Navega por cada URL de categoría del catálogo, activa la vista compacta, y hace scroll infinito para ir cargando todos los links de las obras, y guardar las URLs en `artwork_links.txt`.

**Fase 2 – Scraping de detalle** Para cada URL de la Fase 1, navega a la página de la obra, extrae los metadatos y los guarda en el CSV de salida hasta completar el dataset.

------

## Archivos de estado (checkpoints)

En caso que de que el  scraper deje de funcionar, al relanzarlo, revisa tanto los links como las obras pendientes y lo retome desde ese punto.

| Archivo                              | Contenido                       |
| ------------------------------------ | ------------------------------- |
| `artwork_links.txt`                  | URLs de detalle de cada obra    |
| `scraped_artwork_links_register.txt` | URLs de categoría ya procesadas |
| `scraped_artworks_register.txt`      | URLs de obra ya scrapeadas      |

Si la aplicación cae o se interrumpe, al volver a ejecutar `main.py` retoma exactamente donde lo dejó, sin reprocesar ni duplicar ningún registro.

------

## Ejemplo de logs (`prado.log`)

```json
{'timestamp': '2026-03-22 15:01:52', 'bot': 'prado', 'level': 'INFO', 'msg': '{"navigating to": "https://www.museodelprado.es/busqueda-obras"}'}
{'timestamp': '2026-03-22 15:02:05', 'bot': 'prado', 'level': 'INFO', 'msg': 'Total artworks: 23003'}
{'timestamp': '2026-03-22 15:02:05', 'bot': 'prado', 'level': 'INFO', 'msg': 'Getting pending artwork links'}
{'timestamp': '2026-03-22 15:02:09', 'bot': 'prado', 'level': 'INFO', 'msg': 'Executing infinite scroll using JS'}
{'timestamp': '2026-03-22 15:02:14', 'bot': 'prado', 'level': 'INFO', 'msg': 'Loaded 60 elements on the web'}
{'timestamp': '2026-03-22 15:02:20', 'bot': 'prado', 'level': 'INFO', 'msg': 'Loaded 80 elements on the web'}
{'timestamp': '2026-03-22 15:02:26', 'bot': 'prado', 'level': 'INFO', 'msg': 'Loaded 100 elements on the web'}
```

------

## Ejemplo de links recolectados (`artwork_links.txt`)

```
https://www.museodelprado.es/coleccion/obra-de-arte/joven-dormida-en-una-hamaca/33fbbc26-1744-468d-8366-c6ea93f2434c
https://www.museodelprado.es/coleccion/obra-de-arte/san-roque/73d5dfab-a45b-48be-9696-5abdf4f16ea5
https://www.museodelprado.es/coleccion/obra-de-arte/sagrada-familia-del-pajarito/8008380e-fef5-48b4-8caf-d78b810fb62c
https://www.museodelprado.es/coleccion/obra-de-arte/ataque-naval-a-genova-dirigido-por-el-marques/7d650584-b429-4da0-824c-ee3f6556bbc3
```

------

## Ejemplo de dataset (`dataset/prado_artworks.csv`)

| Número de catálogo | Autor                | Título                               | Fecha      | Técnica             | Dimensión                    |
| ------------------ | -------------------- | ------------------------------------ | ---------- | ------------------- | ---------------------------- |
| P000183            | Luca Giordano        | Toma de una plaza fuerte             | Hacia 1697 | Óleo                | Ancho: 343 cm ; Alto: 235 cm |
| P006870            | Carlos de Haes       | Pinares (San Vicente de la Barquera) | Hacia 1872 | Óleo                | Alto: 32,5 cm ; Ancho: 42 cm |
| D006512            | Élie-Honoré Montagny | La muerte de Viriato                 | Siglo XIX  | Pluma ; Tinta china | Alto: 330 mm ; Ancho: 495 mm |
