# Web Scraping Template with Playwright

Este es un **scraper web** personalizable construido con [Python](https://www.python.org/) y [Playwright](https://playwright.dev/). Diseñado para extraer datos de sitios web con paginación, preservando el estado del progreso y exportando los resultados a CSV de manera incremental.

## 🚀 Características

- **Persistencia de Estado**: Guarda automáticamente el progreso (página actual y URLs procesadas) en `scraping_state.json`. Si el proceso se interrumpe, puedes reanudarlo sin duplicar trabajo.
- **Exportación a CSV**: Los datos extraídos se guardan en tiempo real en `scraping_results.csv`.
- **Optimización de Rendimiento**: Bloquea la carga de imágenes para acelerar la navegación y reducir el consumo de ancho de banda.
- **Manejo de Errores**: 
  - Detecta y maneja errores HTTP (404, 500).
  - Evita reprocesar URLs ya visitadas.
  - Cierra pestañas secundarias automáticamente, incluso si ocurre un error.
- **Navegación por Paginación**: Lógica integrada para navegar a través de múltiples páginas de resultados.

## 📋 Requisitos Previos

-  Creado con Python 3.12
- [uv](https://github.com/astral-sh/uv) (Opcional, pero recomendado para gestión de dependencias)

## 🛠️ Instalación

1. **Clonar el repositorio o descargar los archivos.**

2. **Instalar dependencias:**

   Si usas `uv`:
   ```bash
   uv sync
   ```

   O con `pip` tradicional:
   ```bash
   pip install playwright
   playwright install chromium
   ```

## ⚙️ Configuración

El archivo `main.py` contiene marcadores de posición que **debes configurar** para adaptarlo a tu objetivo de scraping:

1. **URL Objetivo**: 
   Edita la variable `url` en la línea 12 con la dirección web inicial.
   ```python
   url = "https://ejemplo.com/lista-items"
   ```

2. **Selectores**:
   Busca los comentarios `# Completar con el selector adecuado` y llena los métodos `locator()` con los atributos de los elementos de la página objetivo:
   - **Elementos de lista** (línea 48): El contenedor de cada ítem a extraer.
   - **Título/Datos** (línea 65): El dato específico dentro de la página de detalle.
   - **Paginación** (líneas 103, 114): Selectores para el número de página actual/total y el botón "Siguiente".

3. **Base URL** (Opcional):
   Si los enlaces extraídos son relativos (ej: `/item/1`), configura `base_url` en la línea 53.

4. **Personaliza para tu necesidad**:
   Esta plantilla es una estructura minimalista, puedes personalizarla para adaptarla a tus necesidades y a tu página objetivo ya que no todos los sitios web tienen la misma estructura y selectores. Puedes agregar más selectores, funciones, pestañas, etc. 

## ▶️ Uso

Ejecuta el script principal:

Si usas `uv`:
   ```bash
   uv run main.py
   ```

Si usas `pip`:
```bash
python main.py
```

- El scraper abrirá un navegador Chromium (visible por defecto para depuración).
- Verás el progreso en la consola.
- Los datos se guardarán en `scraping_results.csv`.
- El estado (para reanudar) se guarda en `scraping_state.json`.

## 📂 Estructura del Proyecto

- `main.py`: Lógica principal del scraper, flujo de navegación y extracción.
- `progress_state.py`: Módulos auxiliares para cargar/guardar el estado JSON y manejar la escritura CSV.
- `scraping_results.csv`: Archivo de salida (se genera automáticamente).
- `scraping_state.json`: Archivo de control de progreso (se genera automáticamente).

## ⚠️ Notas Importantes

- Este script está configurado con `headless=False` (línea 14) para que veas el navegador trabajar. Para producción o mayor velocidad, cámbialo a `headless=True`.
- Asegúrate de respetar los términos de servicio (ToS) y el archivo `robots.txt` del sitio web que estás scrapeando.
