from machine import Pin, ADC, PWM
import time

# 1. Configurar los 3 canales de LEDs (según tu esquema)
led_amarillo = Pin(25, Pin.OUT)
led_rojo = Pin(26, Pin.OUT)
led_verde = Pin(27, Pin.OUT)

# 2. Configurar el sensor de luz (Fotorresistencia en GPIO34)
sensor_luz = ADC(Pin(34))
sensor_luz.atten(ADC.ATTN_11DB)

# 3. Configurar el Buzzer pasivo en GPIO18
buzzer = PWM(Pin(18))
buzzer.duty(0)

# Frecuencias de las notas musicales (en Hz)
DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392

# Melodía: (Nota, Duración en segundos, LED que enciende)
jingle_bells = [
    # "Na-vi-dad, na-vi-dad"
    (MI, 0.25, led_amarillo),
    (MI, 0.25, led_rojo),
    (MI, 0.50, led_verde),
    (MI, 0.25, led_amarillo),
    (MI, 0.25, led_rojo),
    (MI, 0.50, led_verde),
    
    # "Hoy es na-vi-dad"
    (MI, 0.25, led_amarillo),
    (SOL, 0.25, led_rojo),
    (DO, 0.35, led_verde),
    (RE, 0.15, led_amarillo),
    (MI, 0.80, led_rojo),

    # "Es un dí-a de a-le-grí-a"
    (FA, 0.25, led_verde),
    (FA, 0.25, led_amarillo),
    (FA, 0.35, led_rojo),
    (FA, 0.15, led_verde),
    (FA, 0.25, led_amarillo),
    (MI, 0.25, led_rojo),
    (MI, 0.25, led_verde),
    (MI, 0.15, led_amarillo),

    # "Y fe-li-ci-dad"
    (MI, 0.25, led_rojo),
    (RE, 0.25, led_verde),
    (RE, 0.25, led_amarillo),
    (MI, 0.25, led_rojo),
    (RE, 0.50, led_verde),
    (SOL, 0.60, led_amarillo)
]

def apagar_todo():
    led_amarillo.value(0)
    led_rojo.value(0)
    led_verde.value(0)

def tocar_cancion():
    for nota, duracion, led in jingle_bells:
        # Si mientras suena hay mucha luz, detiene la canción
        if sensor_luz.read() >= 1500:
            break
            
        apagar_todo()
        led.value(1)            # Enciende el LED correspondiente
        buzzer.freq(nota)       # Pone el tono de la nota
        buzzer.duty(512)        # Enciende el sonido
        time.sleep(duracion)    # Espera lo que dura la nota
        
        buzzer.duty(0)          # Pequeña pausa para separar cada nota
        apagar_todo()
        time.sleep(0.06)

print("Iniciando Pino de Navidad Musical...")

while True:
    nivel_luz = sensor_luz.read()
    print("Nivel de luz:", nivel_luz)

    if nivel_luz < 1500:
        tocar_cancion()
        time.sleep(0.5) # Pausa breve antes de repetir el coro
    else:
        apagar_todo()
        buzzer.duty(0)
        time.sleep(0.5)