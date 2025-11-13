from PySide6.QtWidgets import ( QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, 
                               QComboBox, QLineEdit, QScrollArea)
from View.Components.Visual3D import Visual3D
from View.Components.GraficaGenerica import GraficaGenerica
from View.Components.GraficaMaximo import GraficaMaximo
from View.Components.Mapas.LocalizacionGPS import LocalizacionGPS
from PySide6.QtWidgets import QMessageBox  

from Tools.Paths import rutaAbsoluta

#clase para la ventana de monitoreo en timpo real
class MonitoreoTiempoReal(QWidget):
    def __init__(self, controlador):
        super().__init__() # se manda a llamar el constructor la clase Qwidget 
        self.setMinimumSize(1400,650)
        #ajustes de la ventana
        ContenidoPrincipal = QHBoxLayout() # contenedor horizontal que lleva todo el contenido
        ladoIzq = QVBoxLayout() # contenedor vertical para el modelos 3d 
        ladoDer = QVBoxLayout() # contenedor en tabla para las graficas que se van a colocar

        # controlador de la ventana
        self.controlador = controlador # se recive la intancia del controlador
        self.controlador.vista = self # se le pasa la referencia de esta misma ventana

        #----------------------------------componentes lado IZQ------------------------------------
        etVisual = QLabel("Monitoreo 3D")
        etVisual.setObjectName("seccion")
        self.visual = Visual3D(rutaAbsoluta("Media/Model3D/CANSAT.stl")) # modelo 3D
        ladoIzq.addWidget(etVisual) # se agrega la etiqueta de seccion
        ladoIzq.addWidget(self.visual) # se agrego al lado derecho


        #----------------------------------componentes lado DER------------------------------------
        # Etiqueta de la sección de datos
        etGraficas = QLabel("Monitoreo de datos")
        etGraficas.setObjectName("seccion")
        ladoDer.addWidget(etGraficas)

        # Primer grid: campos y controles de puerto
        gridControles = QGridLayout()
        
        # Configurar estiramiento de las columnas para que sean proporcionales
        gridControles.setColumnStretch(0, 1)  # Columna de etiquetas
        gridControles.setColumnStretch(1, 3)  # Columna para QLineEdit y QComboBox
        gridControles.setColumnStretch(2, 2)  # Columna para QComboBox y Velocidad
        gridControles.setColumnStretch(3, 2)  # Columna para Botones
        gridControles.setColumnStretch(4, 2)  # Columna para Botones

        # --- Fila 1 ---
        etMision = QLabel("Mision:")
        etMision.setObjectName("etiquetaControl")
        gridControles.addWidget(etMision, 0, 0)
        
        self.nameMision = QLineEdit()
        self.nameMision.setPlaceholderText("Nombre de lanzamiento...")
        self.nameMision.setObjectName("campoText")
        gridControles.addWidget(self.nameMision, 0, 1)

        self.tipoMision = QComboBox()
        self.tipoMision.setObjectName("desplegable")
        self.tipoMision.addItems(["CANSAT", "AVIONICA"])
        self.tipoMision.currentIndexChanged.connect(self.cambiarModelo3D)
        gridControles.addWidget(self.tipoMision, 0, 2)

        self.conectarBut = QPushButton("Conectar")
        self.conectarBut.setObjectName("boton")
        self.conectarBut.clicked.connect(self.controlador.conectar_puerto)
        gridControles.addWidget(self.conectarBut, 0, 3)

        self.desconectarBut = QPushButton("Desconectar")
        self.desconectarBut.setObjectName("boton")
        self.desconectarBut.clicked.connect(self.controlador.desconectar_puerto)
        gridControles.addWidget(self.desconectarBut, 0, 4)

        # --- Fila 2 ---
        etPuertoSerial = QLabel("Puerto serial:")
        etPuertoSerial.setObjectName("etiquetaControl")
        gridControles.addWidget(etPuertoSerial, 1, 0)

        self.puertosSerial = QComboBox()
        self.puertosSerial.setObjectName("desplegable")
        self.puertosSerial.addItems(self.controlador.listar_puertos())
        gridControles.addWidget(self.puertosSerial, 1, 1)
        
        etVelocidad = QLabel("Velocidad:")
        etVelocidad.setObjectName("etiquetaControl")
        gridControles.addWidget(etVelocidad, 1, 2)

        self.velocidad = QComboBox()
        self.velocidad.setObjectName("desplegable")
        self.velocidad.addItems(["1200","2400","4800","9600","19200","38400","57600","115200"])
        gridControles.addWidget(self.velocidad, 1, 3)

        self.actualizarBut = QPushButton("Actualizar")
        self.actualizarBut.setObjectName("boton")
        self.actualizarBut.clicked.connect(self.controlador.actualizar_puertos)
        gridControles.addWidget(self.actualizarBut, 1, 4)

        

        # -------------------- Scroll para la vista de las graficas y GPS ----------------------

        scroll = QScrollArea()
        scroll.setObjectName("scroll")

        scroll.setWidgetResizable(True)

        contenidoScroll = QWidget() # este es el que se la manda al scroll al final para representar en pantalla
        layoutContenido = QHBoxLayout(contenidoScroll)


        # graficas 
        graficasWidget = QWidget()
        gridGrafica = QGridLayout(graficasWidget)
        
        self.temperatura = GraficaGenerica("Temperatura", "Tiempo (s)","Temperatura (°C)", "°C", "#FF5733")
        self.altura = GraficaMaximo("Altura", "Tiempo (s)", "Altura (m)", "m", "#FFFF33")

        self.humedad = GraficaGenerica("Humedad", "Tiempo (s)", "Humedad (%)", "%", "#33A7FF")
        self.presion = GraficaGenerica("Presión", "Tiempo (s)", "Presión (hPa)", "hPa", "#33FF57")
        
        self.calAire = GraficaGenerica("Calidad Aire", "Tiempo (s)", "Concentración (ppm)", "ppm", "#FFFFFF")

        
        # Agregarlas en 2 filas y 5 columnas
        gridGrafica.addWidget(self.temperatura, 0, 0)
        gridGrafica.addWidget(self.humedad,     0, 1)
        gridGrafica.addWidget(self.presion,     0, 2)
        gridGrafica.addWidget(self.calAire,      1, 0)
        gridGrafica.addWidget(self.altura,      1, 1)
        


        # GPS 
        gpsWidget = QWidget()
        layoutGps = QVBoxLayout(gpsWidget)

        self.gps = LocalizacionGPS()
        layoutGps.addWidget(self.gps)

        # Agregar componentes al scroll
        layoutContenido.addWidget(graficasWidget)
        layoutContenido.addWidget(gpsWidget)

        



        scroll.setWidget(contenidoScroll) # meter el contenido al scroll


        # ------------------------ Layout para botones ------------------------------------------------
        botonesLayout = QHBoxLayout()
        self.iniciarBut = QPushButton("Iniciar")
        self.iniciarBut.clicked.connect(self.controlador.iniciar_monitoreo)
        self.iniciarBut.setObjectName("botonControl")

        self.detenerBut = QPushButton("Detener")
        self.detenerBut.clicked.connect(self.controlador.detener_monitoreo)
        self.detenerBut.setObjectName("botonControl")

        botonesLayout.addStretch()
        botonesLayout.addWidget(self.iniciarBut)
        botonesLayout.addWidget(self.detenerBut)

        # Agregar los grids al lado derecho (vertical)
        ladoDer.addLayout(gridControles)
        ladoDer.addWidget(scroll)
        ladoDer.addLayout(botonesLayout)

        # Envolver los layouts en QWidgets para poder aplicarles estilos
        ladoIzqWidget = QWidget()
        ladoIzqWidget.setLayout(ladoIzq)
        ladoIzqWidget.setObjectName("MarcoWidget")

        ladoDerWidget = QWidget()
        ladoDerWidget.setLayout(ladoDer)
        ladoDerWidget.setObjectName("MarcoWidget")

        #agregar las disposiciones a la ventana principal del objeto
        ContenidoPrincipal.addWidget(ladoIzqWidget) # agregar el lado izq
        ContenidoPrincipal.addWidget(ladoDerWidget) # agregar el lado der
        ContenidoPrincipal.setStretch(0, 2)  # ladoIzq (20%)
        ContenidoPrincipal.setStretch(1, 8)  # ladoDer (80%)
        self.setLayout(ContenidoPrincipal) # definir lo que tiene el componente principal

    # obtener el puerto seleccionado 
    def obtener_puerto(self):
        return self.puertosSerial.currentText()
    
    # obtener la velocidad 
    def obtener_velocidad(self):
        return self.velocidad.currentText()
    
    def obtener_nombre(self):
        return self.nameMision.text() # se retorna un texto que sera el nombre del vuelo
    def obtener_modelo(self):
        return self.tipoMision.currentText() # obetenemos el modelo 3D
    
    # mostrar mensaje en pantalla
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "info": # informacion normal
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "warning": # informacion de advertencia
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "critical": # mensaje critico
            QMessageBox.critical(self, titulo, mensaje)
        else: # mensaje default 
            QMessageBox.information(self, titulo, mensaje)

    # escoger que se va a modelar
    def cambiarModelo3D(self):
        seleccionModel = self.tipoMision.currentText()
        if seleccionModel == "CANSAT":
            self.visual.cambiarModelo3D(rutaAbsoluta("Media/Model3D/CANSAT.stl"))
            self.visual.setZoomFijo(1300)
        elif seleccionModel == "AVIONICA":
            self.visual.cambiarModelo3D(rutaAbsoluta("Media/Model3D/COHETE.stl"))
            self.visual.setZoomFijo(2000)

    # agregar nueva informacion
    #gx, gy, gz, tem, humedad, press, alt, calAire, lon, lat
    def actualizarInformacion(self,gx,gy,gz,tem, hum,press, alt, cal, lon, lat):
        self.visual.actualizarOrientacion(gx,gy,gz)
        self.temperatura.agregarDato(tem)
        self.humedad.agregarDato(hum)
        self.presion.agregarDato(press)
        self.altura.agregarDato(alt)
        self.calAire.agregarDato(cal)
        self.gps.cambiarCordenadas(lon, lat)
