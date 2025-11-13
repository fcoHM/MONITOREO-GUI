# logica de ventana monitoreo en tiempo real
from Tools.SerialManager import SerialManager
from PySide6.QtCore import Slot

class CMonitoreoTiempoReal:

    def __init__(self):
        self.serialManager = SerialManager() # herramienta para el manejo de puertos seriales
        self.vista = None
        # Conectar la señal de datos recibidos al slot de actualización
        self.serialManager.linea_recibida.connect(self.procesar_linea)

    
    def actualizar_puertos(self): # actualizar los puertos, mandando una nueva lista
        puertos = self.serialManager.listar_puertos()
        self.vista.puertosSerial.clear()
        self.vista.puertosSerial.addItems(puertos)
    
    def listar_puertos(self): # listar los puertos que estan conectados
        return self.serialManager.listar_puertos()

    def conectar_puerto(self): # conecta un puesrto serial segun le digamos cual
        puerto = self.vista.obtener_puerto()
        velocidad = self.vista.obtener_velocidad()
        self.serialManager.set_baudios(velocidad)
        
        if self.serialManager.conectar(puerto):
            self.serialManager.iniciar_escaneo() # se inicia el escaneo apenas conectar la estacion terrena
            self.vista.mostrar_mensaje("Éxito", f"Conectado a {puerto} a {velocidad} baudios.")
            self.actualizar_puertos()
        else:
            self.vista.mostrar_mensaje("Error", f"No se pudo conectar a {puerto}.", "warning")

    def desconectar_puerto(self): # desconecta el puerto serial que se esta utilizando
        if self.serialManager.desconectar():
            self.vista.mostrar_mensaje("Éxito", "Se cerró la comunicación con el puerto.")
            self.actualizar_puertos()
        else:
            self.vista.mostrar_mensaje("Error", "No se cerró la comunicación con el puerto.", "warning")

    @Slot(str)
    def procesar_linea(self, linea=""):# procesamiento de la cadena de texto
        if not linea:
            return  # si la línea está vacía, no hacer nada

        try:
            # encuentra las posiciones de las etiquetas
            etCU_start = linea.find("CU:")
            etAV_start = linea.find("AV:")

            carga_util_str = ""
            avionica_str = ""

            # extrae las cadenas de datos 
            if etCU_start != -1 and etAV_start != -1:
                if etCU_start < etAV_start: # orden normal
                    # CU: ... AV: ...
                    carga_util_str = linea[etCU_start + 3 : etAV_start].strip()
                    avionica_str = linea[etAV_start + 3 :].strip()
                else: # orden inverso
                    # AV: ... CU: ...
                    avionica_str = linea[etAV_start + 3 : etCU_start].strip()
                    carga_util_str = linea[etCU_start + 3 :].strip()
            elif etCU_start != -1:
                # Solo CU:
                carga_util_str = linea[etCU_start + 3 :].strip()
            elif etAV_start != -1:
                # Solo AV:
                avionica_str = linea[etAV_start + 3 :].strip()
            else:
                # No se encontraron etiquetas
                print(f"Advertencia: No se encontraron etiquetas 'CU:' o 'AV:' en la línea: {linea}")
                return

            # obtener modelo actual para saber que linea mandar a las graficas 
            modelo_actual = self.vista.obtener_modelo()

            datos_str_list = [] # lista en donde se guardaran los datos
            if modelo_actual == "CANSAT":
                if carga_util_str:
                    datos_str_list = carga_util_str.split(',') # separar por comas
            elif modelo_actual == "AVIONICA":
                if avionica_str:
                    datos_str_list = avionica_str.split(',') # seprar por comas
            
            if not datos_str_list:
                # No hay datos para el modelo actual, o la cadena de datos estaba vacía
                return

            datos = [float(valor.strip()) for valor in datos_str_list if valor.strip()] # datos de salida
            print(datos)
            self.actualizar_graficas(datos) # actualizar grafica, se manda a llamar aqui por que esta funcion esta enlazada con la senial de recepcion de cadenas

        except (ValueError, IndexError) as e:
            print(f"Error al procesar la línea de datos: '{linea}'. Error: {e}")


    def actualizar_graficas(self, datos):
            
            # Asegurarse de que hay suficientes datos antes de acceder a ellos
            if len(datos) >= 13: # si es 13 significa que tiene los sensores basicos
                # Acelerometro (no se usan en la GUI, pero se leen)
                # acrx = datos[0]
                # acry = datos[1]
                # acrz = datos[2]

                # Datos del giroscopio para el visualizador 3D
                gx = datos[3]
                gy = datos[4]
                gz = datos[5]

                # Datos de los sensores para las gráficas
                tem = datos[6]
                humedad = datos[7]
                press = datos[8]
                alt = datos[9]
                calAire = datos[10]
                
                # Datos del GPS
                lon = datos[11]
                lat = datos[12]
                # Se envian los datos a la vista para ser actualizados
                self.vista.actualizarInformacion(gx, gy, gz, tem, humedad, press, alt, calAire, lon, lat)
            elif len(datos) > 13: # cuando haya mas de los 13 datos, siguiendo el estandar
                pass
            
        
            else:
                print(f"Advertencia: Se recibieron datos incompletos")

            
        

    def iniciar_monitoreo(self): # inicar el escaneo del puerto serial
        if self.serialManager.iniciar_escaneo():
            self.vista.mostrar_mensaje("Exito", "Se inicio el monitoreo")
        else:
            self.vista.mostrar_mensaje("Error", "No se inicio el monitoreo", "warning")

    

    def detener_monitoreo(self): # detener el ecaneo del puerto serial
        if self.serialManager.detener_escaneo() and self.serialManager.desconectar():
            self.actualizar_puertos()
            self.vista.temperatura.limpiarVista()
            self.vista.visual.limpiarVista()
            self.vista.mostrar_mensaje("Exito", "Se  detuvo el escaneo y se desconecto el puerto")
        else:
            self.vista.mostrar_mensaje("Error", "No se detuvo el escaneo del puerto", "warning")

    