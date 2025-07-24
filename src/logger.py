# src/logger.py

import csv
from datetime import datetime

LOG_FILE = "registro_riego.csv"

def log_riego(evento, temperatura, humedad):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, evento, temperatura, humedad])

def leer_registros():
    try:
        with open(LOG_FILE, "r") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []
