import os
import csv
import json
from datetime import datetime

STATE_FILE = "scraping_state.json"
CSV_FILE = "scraping_results.csv"

# carga el estado previo del scraping si existe scraping_state.json
def load_state()-> dict:
    """Carga el estado del scraping anterior"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_page": 0, "processed_urls": [], "processed_documents_urls": []}

# Guarda el estado actual del scraping en scraping_state.json
def save_state(page_num, processed_urls, processed_documents_urls):
    """Guarda el estado actual"""
    with open(STATE_FILE, 'w') as f:
        json.dump({
            "last_page": page_num,
            "processed_urls": processed_urls,
            "processed_documents_urls": processed_documents_urls,
            "last_update": datetime.now().isoformat()
        }, f, indent=2)

def save_to_csv_init(rows=[]):
    """Inicializa el archivo CSV con encabezados
    @param rows: lista de filas iniciales a guardar
    @type rows: list
    @example: [['Título', 'URL']]
    """
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
# Guarda los datos en CSV
def save_to_csv(data):
    """Guarda los datos en CSV
    @param data: lista de filas a guardar
    @type data: list
    @example: [['Título1', 'URL1'], ['Título2', 'URL2']]"""
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)