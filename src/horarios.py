# src/horarios.py

import json
import os
from datetime import datetime, timedelta
from config import REPOSO_MINUTOS

HORARIOS_FILE = "horarios.json"
REPOSO_FILE = "ultimo_riego.txt"

def cargar_horarios():
    if not os.path.exists(HORARIOS_FILE):
        return []
    with open(HORARIOS_FILE, "r") as f:
        return json.load(f)

def guardar_horarios(lista_horarios):
    with open(HORARIOS_FILE, "w") as f:
        json.dump(lista_horarios, f)

def guardar_ultimo_riego():
    with open(REPOSO_FILE, "w") as f:
        f.write(datetime.now().isoformat())

def tiempo_desde_ultimo_riego():
    if not os.path.exists(REPOSO_FILE):
        return None
    with open(REPOSO_FILE, "r") as f:
        try:
            ultima = datetime.fromisoformat(f.read().strip())
            return (datetime.now() - ultima).total_seconds() / 60  # en minutos
        except:
            return None

def horario_actual_activo():
    """Devuelve True/False si corresponde regar y respeta tiempo de reposo."""
    ahora = datetime.now()
    horarios = cargar_horarios()
    for h in horarios:
        inicio = datetime.strptime(h["hora"], "%H:%M").replace(
            year=ahora.year, month=ahora.month, day=ahora.day
        )
        fin = inicio + timedelta(minutes=h.get("duracion", 5))
        if inicio <= ahora < fin:
            minutos_reposo = tiempo_desde_ultimo_riego()
            if minutos_reposo is None or minutos_reposo >= REPOSO_MINUTOS:
                return True, h.get("duracion", 5)
    return False, 0
