
from PySide6.QtCore import (QObject, Signal)

class GPS(QObject):
    coordenadas_actualizadas = Signal(float, float)
    signalZoom = Signal(int) # senial para hacer o queitar zoom

    def __init__(self):
        super().__init__()
        # se le da una posicion inicial al mapa
        self.lat = 00.0000000
        self.lon = 00.0000000
        # zoom inicial
        self.zoom = 14

    
    def actualizarCordenadas(self, lat, lon):
        # se cambia la posicion a la llegada del GPS
        if lat != 0 and lon != 0: # revisa que niguna de las dos cordenadas sea cero
            if lat != self.lat or lon != self.lon: # revisa que no sea igual a la anterior
                self.lon = lon
                self.lat = lat
                # se emite la senial
                self.coordenadas_actualizadas.emit(lat, lon)

    def masZoom(self): # hacer zoom al mapa
        if self.zoom < 18: # ver que el ql zoom este bajo el rango maximo
            self.zoom +=2
            print(self.zoom)
            self.signalZoom.emit(self.zoom) # emitir la senial

    def menosZoom(self): # quitar zoom del mapa  
        if self.zoom > 8: # ver que el zoom este por encima del rango minimo
            self.zoom -=2
            print(self.zoom)
            self.signalZoom.emit(self.zoom) # emitir la senial

