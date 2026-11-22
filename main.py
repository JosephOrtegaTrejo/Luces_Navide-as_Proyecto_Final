from machine import Pin
import time

led = Pin(2, Pin.OUT)

print("Iniciando prueba de luces navideñas...")

while True:
    led.value(1)   # Enciende el LED
    time.sleep(0.5)
    led.value(0)   # Apaga el LED
    time.sleep(0.5)