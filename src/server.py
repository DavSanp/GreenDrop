# src/server.py

from flask import Flask, jsonify, send_from_directory
from sensors import leer_temperatura_humedad
from relay import activar_relay, desactivar_relay, estado_relay

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    # Servir el dashboard bonito
    return send_from_directory('static', 'index.html')

@app.route('/api/status')
def status():
    temp, hum = leer_temperatura_humedad()
    relay = estado_relay()
    return jsonify({
        "temperatura": temp,
        "humedad": hum,
        "relay": "ON" if relay else "OFF"
    })

@app.route('/api/activar')
def activar():
    activar_relay()
    return jsonify({"relay": "ON"})

@app.route('/api/desactivar')
def desactivar():
    desactivar_relay()
    return jsonify({"relay": "OFF"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

