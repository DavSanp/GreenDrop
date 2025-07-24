# src/server.py

from flask import Flask, jsonify, send_from_directory, request
from sensors import leer_temperatura_humedad
from relay import activar_relay, desactivar_relay, estado_relay
from logger import leer_registros
from horarios import cargar_horarios, guardar_horarios, es_hora_de_riego
import threading
import time
import os

app = Flask(__name__, static_folder="static")

# Umbral persistente
UMBRAL = 40.0
UMBRAL_FILE = "umbral.txt"

def cargar_umbral():
    global UMBRAL
    if os.path.exists(UMBRAL_FILE):
        with open(UMBRAL_FILE) as f:
            try:
                UMBRAL = float(f.read().strip())
            except:
                pass

def guardar_umbral(valor):
    with open(UMBRAL_FILE, "w") as f:
        f.write(str(valor))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/status')
def status():
    temp, hum = leer_temperatura_humedad()
    relay = estado_relay()
    return jsonify({
        "temperatura": temp,
        "humedad": hum,
        "umbral": UMBRAL,
        "relay": "ON" if relay else "OFF"
    })

@app.route('/api/riego', methods=['POST'])
def set_riego():
    data = request.get_json()
    accion = data.get("accion", "").upper()
    if accion == "ON":
        activar_relay()
    elif accion == "OFF":
        desactivar_relay()
    else:
        return jsonify({"error": "Acción inválida"}), 400
    return jsonify({"relay": "ON" if estado_relay() else "OFF"})

@app.route('/api/umbral', methods=['POST'])
def set_umbral():
    global UMBRAL
    data = request.get_json()
    nuevo_umbral = data.get("umbral")
    try:
        nuevo_umbral = float(nuevo_umbral)
        UMBRAL = nuevo_umbral
        guardar_umbral(UMBRAL)
        return jsonify({"umbral": UMBRAL})
    except:
        return jsonify({"error": "Umbral inválido"}), 400

@app.route("/api/registros", methods=["GET"])
def api_registros():
    registros = leer_registros()
    return jsonify({"registros": registros})

@app.route("/api/horarios", methods=["GET"])
def get_horarios():
    return jsonify({"horarios": cargar_horarios()})

@app.route("/api/horarios", methods=["POST"])
def set_horarios():
    data = request.get_json()
    horarios = data.get("horarios")
    if not isinstance(horarios, list):
        return jsonify({"error": "Formato inválido"}), 400
    guardar_horarios(horarios)
    return jsonify({"ok": True})

# Thread para riego programado
def riego_programado():
    while True:
        if es_hora_de_riego():
            if not estado_relay():
                activar_relay()
        else:
            if estado_relay():
                desactivar_relay()
        time.sleep(60)

if __name__ == "__main__":
    cargar_umbral()
    t = threading.Thread(target=riego_programado, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
