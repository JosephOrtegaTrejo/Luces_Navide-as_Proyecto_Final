from machine import Pin, ADC, PWM
import time

# 1. Configurar los 3 canales de LEDs (según tu esquema)
led_amarillo = Pin(25, Pin.OUT)
led_rojo = Pin(26, Pin.OUT)
led_verde = Pin(27, Pin.OUT)

# 2. Configurar el sensor de luz (Fotorresistencia en GPIO34)
sensor_luz = ADC(Pin(34))
sensor_luz.atten(ADC.ATTN_11DB) # Permite leer todo el rango de 0 a 3.3V

# 3. Configurar el Buzzer pasivo en GPIO18
buzzer = PWM(Pin(18))
buzzer.duty(0) # Empieza apagado

# Función sencilla para tocar una nota
def tocar_nota(frecuencia, duracion):
    if frecuencia == 0:
        buzzer.duty(0)
    else:
        buzzer.freq(frecuencia)
        buzzer.duty(512) # Volumen medio
    time.sleep(duracion)
    buzzer.duty(0)

# Función para apagar todas las luces
def apagar_todo():
    led_amarillo.value(0)
    led_rojo.value(0)
    led_verde.value(0)

print("Iniciando Pino de Navidad...")

while True:
    # Leer cuánta luz hay (0 = muy oscuro, 4095 = mucha luz)
    nivel_luz = sensor_luz.read()
    print("Nivel de luz:", nivel_luz)

    # Si está oscuro (puedes cambiar el 1500 según tus pruebas)
    if nivel_luz < 1500:
        # Secuencia navideña básica + notas (Jingle Bells: Mi, Mi, Mi)
        led_amarillo.value(1)
        tocar_nota(330, 0.25) # Nota Mi
        apagar_todo()
        time.sleep(0.1)

        led_rojo.value(1)
        tocar_nota(330, 0.25) # Nota Mi
        apagar_todo()
        time.sleep(0.1)

        led_verde.value(1)
        tocar_nota(330, 0.5)  # Nota Mi larga
        apagar_todo()
        time.sleep(0.3)
    else:
        # Si hay mucha luz, todo se queda apagado
        apagar_todo()
        buzzer.duty(0)
        time.sleep(0.5)