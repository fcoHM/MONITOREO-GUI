from PySide6.QtWidgets import(QWidget,QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton)
from PySide6.QtCore import QUrl
from View.Components.Mapas.GPS import GPS
from PySide6.QtQuickWidgets import QQuickWidget
from Tools.Paths import rutaAbsoluta

class LocalizacionGPS(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(900,400) # tamanio minimo del gps
        # Layout principal
        contenido = QVBoxLayout(self)

        # Vista del mapa
        self.mapa = QQuickWidget()
        self.mapa.setResizeMode(QQuickWidget.SizeRootObjectToView)
        contenido.addWidget(self.mapa) # se agrega el mapa


        # Adjuntamos la clase de gps
        self.gps = GPS()
        self.mapa.rootContext().setContextProperty("gps", self.gps)

        # Le damos el mapa al contexto de la vista rapida
        rutaMapa = rutaAbsoluta("View/Components/Mapas/Mapa.qml")
        qml_url = QUrl.fromLocalFile(rutaMapa)
        self.mapa.setSource(qml_url)

        # layout de control
        self.controlLayout = QHBoxLayout() # etiqueta de monitoreo
        self.etiCordenadas = QLabel(f"Lon: -000:00000000  Lat: -000:00000000")
        self.etiCordenadas.setObjectName("EstiInfo")

        self.zoomMas = QPushButton("+") # aumentar zoom
        self.zoomMas.clicked.connect(self.gps.masZoom)
        self.zoomMas.setObjectName("botonControl")

        self.zoomMenos = QPushButton("-") # disminuir zoom
        self.zoomMenos.clicked.connect(self.gps.menosZoom)
        self.zoomMenos.setObjectName("botonControl")
        
        self.controlLayout.addWidget(self.etiCordenadas)
        self.controlLayout.addWidget(self.zoomMenos)
        self.controlLayout.addWidget(self.zoomMas)

        contenido.addLayout(self.controlLayout) # se agrega el panel de control al contenido

    def cambiarCordenadas(self, lon, lat):
        self.etiCordenadas.setText(f"Lat: {lat}, Lon: {lon}")
        self.gps.actualizarCordenadas(lat, lon)

    