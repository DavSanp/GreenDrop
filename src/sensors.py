# src/sensors.py

import board
import adafruit_dht

DHT_PIN = board.D4
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

def leer_temperatura_humedad():
    try:
        temperatura = dhtDevice.temperature
        humedad = dhtDevice.humidity
        return temperatura, humedad
    except Exception as e:
        print("Error leyendo sensor:", e)
        return None, None

