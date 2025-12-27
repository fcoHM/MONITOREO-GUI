from PySide6.QtWidgets import (QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout)
from PySide6.QtCore import Slot


class GraficaBateria(QWidget):

    def __init__(self):
        # carateristicas de la ventana
        super().__init__()
        self.etBateria = QLabel('Nivel bateria')
        self.etBateria.setObjectName("etiquetaControl")
        self.layout = QVBoxLayout() # el contenido se vera hacia arriba
        layout_contenido = QHBoxLayout() # se vera de manera horizontal
        
        # componentes de mostrar bateria
        self.b1 = QFrame()
        self.b2 = QFrame()
        self.b3 = QFrame()
        self.b4 = QFrame()
        self.b5 = QFrame()
        self.b6 = QFrame()
        self.b7 = QFrame()
        self.b8 = QFrame()
        self.b9 = QFrame()

        self.baterias = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]
        
        for bateria in self.baterias:
            bateria.setFixedWidth(30)
            bateria.setStyleSheet("background-color: white;") # color default
            layout_contenido.addWidget(bateria) # Agregando las barras al layout horizontal

        self.layout.addWidget(self.etBateria, 15)
        self.layout.addLayout(layout_contenido, 85)
        self.setLayout(self.layout)

        self._level = 0
        self.set_battery_level(0) # Inicializar con nivel 0

    def get_battery_level(self):
        return self._level

    @Slot(int) 
    def set_battery_level(self, level):
        self._level = level
        #  logica del cambio del color