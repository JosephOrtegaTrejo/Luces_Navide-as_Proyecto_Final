from machine import Pin, ADC, PWM
from ble_control import ControlBluetooth  # Importamos el archivo del Bluetooth
import time

# 1. Configurar los 3 canales de LEDs (según tu esquema)[cite: 8]
led_amarillo = Pin(25, Pin.OUT)
led_rojo = Pin(26, Pin.OUT)
led_verde = Pin(27, Pin.OUT)

# 2. Configurar el sensor de luz (Fotorresistencia en GPIO34)[cite: 8]
sensor_luz = ADC(Pin(34))
sensor_luz.atten(ADC.ATTN_11DB)

# 3. Configurar el Buzzer pasivo en GPIO18[cite: 8]
buzzer = PWM(Pin(18))
buzzer.duty(0)

# 4. Iniciar el módulo Bluetooth
bt = ControlBluetooth("Pino_Navidad")

# Frecuencias de las notas musicales (en Hz)
DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392

# Melodía completa: (Nota, Duración en segundos, LED que enciende)
jingle_bells = [
    (MI, 0.25, led_amarillo), (MI, 0.25, led_rojo), (MI, 0.50, led_verde),
    (MI, 0.25, led_amarillo), (MI, 0.25, led_rojo), (MI, 0.50, led_verde),
    (MI, 0.25, led_amarillo), (SOL, 0.25, led_rojo), (DO, 0.35, led_verde),
    (RE, 0.15, led_amarillo), (MI, 0.80, led_rojo),

    (FA, 0.25, led_verde), (FA, 0.25, led_amarillo), (FA, 0.35, led_rojo),
    (FA, 0.15, led_verde), (FA, 0.25, led_amarillo), (MI, 0.25, led_rojo),
    (MI, 0.25, led_verde), (MI, 0.15, led_amarillo),

    (MI, 0.25, led_rojo), (RE, 0.25, led_verde), (RE, 0.25, led_amarillo),
    (MI, 0.25, led_rojo), (RE, 0.50, led_verde), (SOL, 0.60, led_amarillo),

    (MI, 0.25, led_amarillo), (MI, 0.25, led_rojo), (MI, 0.50, led_verde),
    (MI, 0.25, led_amarillo), (MI, 0.25, led_rojo), (MI, 0.50, led_verde),
    (MI, 0.25, led_amarillo), (SOL, 0.25, led_rojo), (DO, 0.35, led_verde),
    (RE, 0.15, led_amarillo), (MI, 0.80, led_rojo),

    (FA, 0.25, led_verde), (FA, 0.25, led_amarillo), (FA, 0.35, led_rojo),
    (FA, 0.15, led_verde), (FA, 0.25, led_amarillo), (MI, 0.25, led_rojo),
    (MI, 0.25, led_verde), (MI, 0.15, led_amarillo),

    (SOL, 0.25, led_rojo), (SOL, 0.25, led_verde), (FA, 0.25, led_amarillo),
    (RE, 0.25, led_rojo), (DO, 0.80, led_verde)
]

def apagar_todo():
    led_amarillo.value(0)
    led_rojo.value(0)
    led_verde.value(0)

def debe_encender():
    if bt.modo == "ON":
        return True
    elif bt.modo == "OFF":
        return False
    else:  # Modo AUTO (depende de la fotorresistencia)[cite: 6, 8]
        return sensor_luz.read() < 1500

def tocar_cancion():
    for nota, duracion, led in jingle_bells:
        if not debe_encender():
            break
            
        apagar_todo()
        led.value(1)
        buzzer.freq(nota)
        buzzer.duty(512)
        time.sleep(duracion)
        
        buzzer.duty(0)
        apagar_todo()
        time.sleep(0.06)

print("Iniciando Pino de Navidad con Bluetooth...")

while True:
    if debe_encender():
        tocar_cancion()
        time.sleep(0.5)
    else:
        apagar_todo()
        buzzer.duty(0)
        time.sleep(0.3)