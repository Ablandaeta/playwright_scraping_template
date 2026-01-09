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
- **Logging con Iconos**: Sistema de logging visual con emojis para fácil seguimiento del progreso.
- **Seguimiento de Tiempo**: Muestra el tiempo de ejecución al finalizar o en caso de error.

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

El archivo `main.py` está organizado en secciones claramente definidas. Aquí están los elementos que **debes configurar**:

### 1. Constantes de Configuración (líneas 18-34)

```python
# =============================================================================
# CONFIGURACIÓN
# =============================================================================
BASE_URL = "https://www.example.com"
TARGET_URL = "https://www.example.com/page=1"
PAGE_LOAD_TIMEOUT = 3000  # ms
ELEMENT_LOAD_TIMEOUT = 1500  # ms
INTER_REQUEST_DELAY = 500  # ms

# Encabezados de columnas CSV
CSV_HEADERS = [["Título", "Fecha", "Document_URL"]]

# Configuración del navegador
BROWSER_CONFIG = {
    "headless": False,
    # "executable_path": r"C:\ruta\a\navegador.exe",  # Opcional
}
```

| Variable | Descripción |
|----------|-------------|
| `BASE_URL` | URL base del sitio (para construir URLs relativas) |
| `TARGET_URL` | URL inicial con paginación (ej: `page=1`) |
| `PAGE_LOAD_TIMEOUT` | Tiempo de espera después de cargar página principal (ms) |
| `ELEMENT_LOAD_TIMEOUT` | Tiempo de espera después de cargar página de elemento (ms) |
| `INTER_REQUEST_DELAY` | Delay entre peticiones para evitar bloqueos (ms) |
| `CSV_HEADERS` | Encabezados de las columnas del CSV de salida |
| `BROWSER_CONFIG` | Configuración de Playwright (headless, executable_path, etc.) |

### 2. Selectores (busca `TODO:`)

Debes completar los selectores de Playwright en estas líneas:

| Línea | Propósito | Ejemplo |
|-------|-----------|---------|
| 170 | Elementos de lista a procesar | `page.locator('a.item-link').all()` |
| 205 | URL del documento | `element_page.locator('a.download-btn')` |
| 206 | Título del elemento | `element_page.locator('h1.title')` |
| 207 | Fecha del elemento | `element_page.locator('span.date')` |
| 252 | Información de paginación | `page.locator('span.page-info')` |

### 3. Alternativas Comentadas

El código incluye alternativas comentadas para diferentes escenarios:

- **Paginación por URL vs botón** (líneas 152-155, 259-266)
- **URLs relativas vs absolutas** (línea 175)
- **Abrir pestañas con middle-click** (líneas 191-195)

## 📂 Estructura del Proyecto

```
Web Scraping/
├── main.py              # Lógica principal del scraper
├── progress_state.py    # Módulo de gestión de estado y CSV
├── scraping_results.csv # Archivo de salida (auto-generado)
├── scraping_state.json  # Estado de progreso (auto-generado)
├── pyproject.toml       # Dependencias del proyecto
└── README.md            # Este archivo
```

### Estructura de `main.py`

El archivo está organizado en secciones:

```
┌─────────────────────────────────────┐
│ CONFIGURACIÓN                       │  ← Constantes y configuración
├─────────────────────────────────────┤
│ FUNCIONES UTILITARIAS               │  
│  • create_route_interceptor()       │  ← Bloquea imágenes
│  • create_new_page()                │  ← Crea páginas con interceptor
│  • log_progress()                   │  ← Logging con iconos
│  • log_time()                       │  ← Registra tiempo de ejecución
├─────────────────────────────────────┤
│ LÓGICA PRINCIPAL DE SCRAPING        │
│  • run()                            │  ← Función principal
├─────────────────────────────────────┤
│ PUNTO DE ENTRADA                    │
│  • if __name__ == "__main__"        │  ← Ejecución del script
└─────────────────────────────────────┘
```

### Estructura de `progress_state.py`

```
┌─────────────────────────────────────┐
│ CONFIGURACIÓN                       │
│  • STATE_FILE, CSV_FILE             │  ← Nombres de archivos
│  • DEFAULT_STATE                    │  ← Estado inicial
├─────────────────────────────────────┤
│ GESTIÓN DE ESTADO                   │
│  • load_state()                     │  ← Carga estado previo
│  • save_state()                     │  ← Guarda estado actual
├─────────────────────────────────────┤
│ GESTIÓN DE CSV                      │
│  • save_to_csv_init()               │  ← Inicializa CSV con headers
│  • save_to_csv()                    │  ← Añade filas al CSV
└─────────────────────────────────────┘
```

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

### Salida en Consola

El scraper muestra progreso visual con emojis:

```
📌 Tiempo de inicio: 2024-01-09 10:30:00
📌 Iniciando desde la página 1
📊 URLs ya procesadas: 0
📊 Documentos ya procesados: 0
📄 Procesando página 1 (25 elementos)
✅ [1/25] ['Título del artículo', '2024-01-01', 'https://...']
⏭️  [2/25] Ya procesada, saltando...
⚠️  [3/25] No se encontró url
💾 Guardados 23 registros de la página 1
📍 Página 1 de 10
...
✅ ¡Scraping completado!
⏱️  runtime: 0:15:32.456789
📊 Total de registros extraídos: 250
```

## � Funciones Utilitarias

### `log_progress(message, level)`

Sistema de logging con niveles e iconos:

| Level | Icono | Uso |
|-------|-------|-----|
| `info` | 📄 | Información general |
| `success` | ✅ | Operación exitosa |
| `warning` | ⚠️ | Advertencias |
| `error` | ❌ | Errores |
| `skip` | ⏭️ | Elementos saltados |
| `save` | 💾 | Datos guardados |
| `start` | 📌 | Inicio de proceso |
| `stats` | 📊 | Estadísticas |
| `nav` | ⏩ | Navegación |
| `page` | 📍 | Información de página |
| `time` | ⏱️ | Tiempo de ejecución |

### `log_time(start_time)`

Calcula y muestra el tiempo transcurrido desde `start_time`.

### `create_new_page(browser, route_interceptor)`

Crea una nueva página con el interceptor de imágenes configurado.

## ⚠️ Notas Importantes

- Este script está configurado con `headless=False` para que veas el navegador trabajar.
- Puedes especificar un navegador diferente (Chrome, Brave, Edge) usando `executable_path` en `BROWSER_CONFIG`.
- Asegúrate de respetar los términos de servicio (ToS) y el archivo `robots.txt` del sitio web que estás scrapeando.
- El código incluye type hints para mejor mantenibilidad y autocompletado en IDEs.

## 📝 Licencia

Este proyecto es una plantilla de uso libre. Modifícalo según tus necesidades.
