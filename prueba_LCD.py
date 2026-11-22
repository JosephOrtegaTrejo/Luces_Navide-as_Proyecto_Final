from machine import Pin, SoftI2C
import time

# 1. Configurar bus I2C en los pines de tu esquema (SCL=22, SDA=21)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Detectar automáticamente la dirección de la pantalla (suele ser 0x27 o 0x3F)
dispositivos = i2c.scan()
if not dispositivos:
    print("Error: No se detectó la pantalla LCD. Revisa los cables SDA, SCL, VCC y GND.")
else:
    direccion = dispositivos[0]
    print("Pantalla detectada en dirección:", hex(direccion))

    # Controlador mínimo integrado para módulo PCF8574
    def lcd_enviar(datos, modo=0):
        alto = (datos & 0xF0) | modo | 0x08
        bajo = ((datos << 4) & 0xF0) | modo | 0x08
        for val in (alto, alto | 0x04, alto, bajo, bajo | 0x04, bajo):
            i2c.writeto(direccion, bytes([val]))
            time.sleep_us(50)

    def lcd_iniciar():
        time.sleep_ms(20)
        for cmd in (0x33, 0x32, 0x28, 0x0C, 0x06, 0x01):
            lcd_enviar(cmd, 0)
            time.sleep_ms(5)

    def lcd_escribir(texto, linea=0):
        lcd_enviar(0x80 if linea == 0 else 0xC0, 0)
        for letra in texto:
            lcd_enviar(ord(letra), 1)

    # Iniciar y mostrar tu mensaje
    lcd_iniciar()
    lcd_escribir("Prueba 1 Pantalla", 0)
    print("Mensaje enviado a la pantalla.")
    