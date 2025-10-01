import serial
from serial.tools.list_ports import comports
from threading import Thread, Event
import time
from PySide6.QtCore import QObject, Signal

# esta clase se encargar del manejo del puerto serial
class SerialManager(QObject):
    linea_recibida = Signal(str)

    def __init__(self):
        super().__init__()
        self.serialConexion = None  # conexion serial activa
        self.scanning_thread = None  # hilo que escanea en segundo plano
        self.scanning_event = Event()  # bandera para detener el hilo
        self.baudios = 1200  # veolocidad de trasmicion por defecto

# metodos funcionales

    # se encarga de regresar una lista de solo aquellos puertos que responden
    def listar_puertos(self):
        puertos = comports()  # lista todos los puertos
        puertos_activos = []

        for puerto in puertos:  # se itera sobre todos los puertos existentes
            try:
                # trata de hablar con el perto
                with serial.Serial(puerto.device, self.baudios, timeout=0.5):
                    # si el puerto responde se agrega a la lista de activos
                    puertos_activos.append(puerto.device)
            except (serial.SerialException, OSError):
                continue  # si falla pasa al siguiente puerto

        return puertos_activos  # se retorna la lista de los puertos activos

    # establecer comunicasion con un puerto
    def conectar(self, puerto):
        if self.serialConexion and self.serialConexion.is_open:
            self.desconectar()  # desconectamos el puerto

        try:
            self.serialConexion = serial.Serial(
                port=puerto,  # puerto seleccionado
                baudrate=self.baudios,  # velocidad
                timeout=0.5 # Timeout de lectura en segundos
            )
            return True  # si se establecio
        except serial.SerialException:
            return False  # no se establecion

    # desconectar el puerto con el que se tiene comunicasion
    def desconectar(self):
        if self.serialConexion and self.serialConexion.is_open:
            self.detener_escaneo()  # Detiene el escaneo si está activo
            self.serialConexion.close()
            return True
        return False

    # iniciar escaneo de un puerto serial
    def iniciar_escaneo(self):
        # verifica que no haya una conexion
        if not self.serialConexion or not self.serialConexion.is_open:
            return False

         # verifica que no haya ya un escaneo en curso
        if self.scanning_thread and self.scanning_thread.is_alive():
            print("El escaneo ya está en progreso")
            return False

        # Configura el callback y limpia evento de parada
        self.scanning_event.clear()

        # Crea e inicia el hilo de escaneo
        self.scanning_thread = Thread(target=self._escanear_puerto)
        self.scanning_thread.daemon = True # El hilo terminará si el programa principal lo hace
        self.scanning_thread.start()
        return True

    # detener el escaneo del puerto
    def detener_escaneo(self):
        if self.scanning_thread and self.scanning_thread.is_alive():
            # activa el evento de parada y espera a que termine el hilo
            self.scanning_event.set()
            self.scanning_thread.join(timeout=1)
            return True
        return False

    # escanear puerto
    def _escanear_puerto(self):
        buffer = ""  # este se puede cambiar a un arreglo tipo bytes 

        while not self.scanning_event.is_set():  # Se ejecuta hasta activar evento de parada
            try:
                # verifica si hay datos disponibles
                if self.serialConexion and self.serialConexion.in_waiting > 0:
                    # lee y decodifica los datos disponibles
                    data = self.serialConexion.read( # aqui se puede mandar en crudo y trabajar con bytes
                        self.serialConexion.in_waiting).decode('utf-8', errors='ignore')
                    buffer += data

                    # Procesa líneas completas (separadas por \n)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)  # separa la primera línea
                        line = line.strip()  # elimina espacios y saltos de línea
                        if line:
                            # Emite la señal con la línea completa
                            self.linea_recibida.emit(line)

                time.sleep(0.01)  # pequeña pausa para reducir carga de CPU

            except serial.SerialException:
                print("Error de lectura serial. Desconectando.")
                self.scanning_event.set() # Termina el bucle en caso de error
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                break


# metodos get y set

    # cambiar la volocidad de comunicasion
    def set_baudios(self, baudios):
        self.baudios = baudios  # se cambia el valor de la velocidad

        if self.serialConexion and self.serialConexion.is_open:  # si hay una conexion y esta abierta
            self.serialConexion.baudrate = baudios  # cambia los baudios

# Destructor: asegura que se cierre la conexión al eliminar la instancia.
    def __del__(self):
        self.desconectar()
