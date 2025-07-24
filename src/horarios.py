# src/horarios.py

import json
import os
from datetime import datetime

HORARIOS_FILE = "horarios.json"

def cargar_horarios():
    if not os.path.exists(HORARIOS_FILE):
        return []
    with open(HORARIOS_FILE, "r") as f:
        return json.load(f)

def guardar_horarios(lista_horarios):
    with open(HORARIOS_FILE, "w") as f:
        json.dump(lista_horarios, f)

def es_hora_de_riego():
    ahora = datetime.now()
    hhmm = ahora.strftime("%H:%M")
    horarios = cargar_horarios()
    return hhmm in horarios
