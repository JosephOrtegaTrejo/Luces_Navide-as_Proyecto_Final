from machine import Pin, SoftI2C
import time

class ControlLCD:
    def __init__(self, scl_pin=22, sda_pin=21):
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
        dispositivos = self.i2c.scan()
        self.direccion = dispositivos[0] if dispositivos else None
        self.texto_actual = ""

        if self.direccion:
            print("Pantalla LCD detectada en:", hex(self.direccion))
            self._iniciar()
        else:
            print("Aviso: No se detectó la pantalla LCD.")

    def _enviar(self, datos, modo=0):
        alto = (datos & 0xF0) | modo | 0x08
        bajo = ((datos << 4) & 0xF0) | modo | 0x08
        for val in (alto, alto | 0x04, alto, bajo, bajo | 0x04, bajo):
            self.i2c.writeto(self.direccion, bytes([val]))
            time.sleep_us(50)

    def _iniciar(self):
        time.sleep_ms(20)
        for cmd in (0x33, 0x32, 0x28, 0x0C, 0x06, 0x01):
            self._enviar(cmd, 0)
            time.sleep_ms(5)

    def mostrar(self, linea1, linea2=""):
        # Evita parpadeos innecesarios si el mensaje no ha cambiado
        if not self.direccion or (linea1 + linea2) == self.texto_actual:
            return
        self.texto_actual = linea1 + linea2

        # Limpiar pantalla
        self._enviar(0x01, 0)
        time.sleep_ms(2)

        # Escribir línea 1 (máximo 16 caracteres)
        self._enviar(0x80, 0)
        for letra in linea1[:16]:
            self._enviar(ord(letra), 1)

        # Escribir línea 2 (máximo 16 caracteres)
        if linea2:
            self._enviar(0xC0, 0)
            for letra in linea2[:16]:
                self._enviar(ord(letra), 1)

# Si ejecutas este archivo directamente para probarlo solo, muestra el mensaje:
if __name__ == "__main__":
    lcd = ControlLCD()
    lcd.mostrar("Feliz navidad :)")