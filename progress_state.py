"""
Módulo de Gestión de Estado de Progreso

Proporciona funcionalidad para persistir y cargar el estado del scraping,
permitiendo sesiones de web scraping reanudables.
"""

import csv
import json
import os
from datetime import datetime
from typing import Any


# =============================================================================
# CONFIGURACIÓN
# =============================================================================
STATE_FILE = "scraping_state.json"
CSV_FILE = "scraping_results.csv"

# Estructura de estado por defecto
DEFAULT_STATE: dict[str, Any] = {
    "last_page": 0,
    "processed_urls": [],
    "processed_documents_urls": [],
}


# =============================================================================
# GESTIÓN DE ESTADO
# =============================================================================
def load_state() -> dict[str, Any]:
    """
    Carga el estado previo del scraping desde el archivo de estado.
    
    Returns:
        dict: El estado guardado si existe, de lo contrario el estado por defecto con:
            - last_page (int): Último número de página procesado exitosamente
            - processed_urls (list): Lista de URLs de elementos procesados
            - processed_documents_urls (list): Lista de URLs de documentos procesados
    
    Example:
        >>> state = load_state()
        >>> print(state["last_page"])
        5
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_STATE.copy()


def save_state(
    page_num: int,
    processed_urls: list[str],
    processed_documents_urls: list[str],
) -> None:
    """
    Guarda el estado actual del scraping en el archivo de estado.
    
    Args:
        page_num: El último número de página procesado exitosamente.
        processed_urls: Lista de todas las URLs de elementos procesados.
        processed_documents_urls: Lista de todas las URLs de documentos procesados.
    
    Note:
        Esta función sobrescribe el archivo de estado existente con el nuevo estado.
        El estado incluye una marca de tiempo de la última actualización.
    """
    state = {
        "last_page": page_num,
        "processed_urls": processed_urls,
        "processed_documents_urls": processed_documents_urls,
        "last_update": datetime.now().isoformat(),
    }
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# =============================================================================
# GESTIÓN DE CSV
# =============================================================================
def save_to_csv_init(rows: list[list[str]] | None = None) -> None:
    """
    Inicializa el archivo CSV con las filas de encabezado.
    
    Debe llamarse una vez al inicio de una nueva sesión de scraping
    para crear el archivo CSV con los encabezados de columna apropiados.
    
    Args:
        rows: Lista de filas a escribir como encabezados. Por defecto lista vacía.
    
    Example:
        >>> save_to_csv_init([["Título", "Fecha", "URL"]])
    """
    if rows is None:
        rows = []
    
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def save_to_csv(data: list[list[str]]) -> None:
    """
    Añade filas de datos al archivo CSV.
    
    Args:
        data: Lista de filas a añadir, donde cada fila es una lista de strings.
    
    Example:
        >>> save_to_csv([
        ...     ["Artículo 1", "2024-01-01", "https://example.com/1"],
        ...     ["Artículo 2", "2024-01-02", "https://example.com/2"],
        ... ])
    """
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)