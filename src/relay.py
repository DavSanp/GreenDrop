# src/relay.py

import RPi.GPIO as GPIO

RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def activar_relay():
    GPIO.output(RELAY_PIN, GPIO.HIGH)

def desactivar_relay():
    GPIO.output(RELAY_PIN, GPIO.LOW)

def estado_relay():
    return GPIO.input(RELAY_PIN) == GPIO.HIGH

