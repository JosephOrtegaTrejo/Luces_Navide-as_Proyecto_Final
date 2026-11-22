import bluetooth

class ControlBluetooth:
    def __init__(self, nombre="Pino_Navidad"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.nombre = nombre
        self.modo = "AUTO"  # Empieza en modo automático (sensor de luz)
        self.conexiones = set()

        # UUIDs estándar para puerto serie virtual (UART)
        uuid_servicio = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        uuid_rx = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)
        uuid_tx = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)

        ((self.handle_tx, self.handle_rx),) = self.ble.gatts_register_services(((uuid_servicio, (uuid_tx, uuid_rx)),))
        self.ble.irq(self._evento)
        self._anunciar()

    def _anunciar(self):
        payload = bytearray(b'\x02\x01\x06') + bytearray((len(self.nombre) + 1, 0x09)) + self.nombre.encode()
        self.ble.gap_advertise(100000, adv_data=payload)

    def _evento(self, evento, datos):
        if evento == 1:  # Celular conectado
            conn_handle, _, _ = datos
            self.conexiones.add(conn_handle)
            print("Celular conectado por Bluetooth")
        elif evento == 2:  # Celular desconectado
            conn_handle, _, _ = datos
            self.conexiones.discard(conn_handle)
            print("Celular desconectado")
            self._anunciar()
        elif evento == 3:  # Mensaje recibido
            conn_handle, value_handle = datos
            if value_handle == self.handle_rx:
                comando = self.ble.gatts_read(self.handle_rx).decode().strip().upper()
                print("Comando Bluetooth recibido:", comando)
                if comando in ("ON", "1"):
                    self.modo = "ON"
                elif comando in ("OFF", "0"):
                    self.modo = "OFF"
                elif comando in ("AUTO", "A"):
                    self.modo = "AUTO"