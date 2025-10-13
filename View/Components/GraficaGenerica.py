from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel) 
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraficaGenerica(QWidget):
    def __init__(self, nombre_grafica, nomX, nomY, notacion, color):
        super().__init__()
        self.setMinimumSize(500, 390)  # Tamaño inicial de la ventana QT
        
        # Contadores para datos y tiempo
        self.tiempos_ventana = []      # Eje X: tiempo en segundos temporales
        self.datos_ventana = []        # Eje Y: datos temporales
        

        self.contador_segundos = 0 # Segundos de la grafica
        self.nombre_grafica = nombre_grafica  # Nombre de la grafica
        self.nombre_eje_x = nomX # Nombre del eje X
        self.nombre_eje_y = nomY # Nombre del eje Y
        self.notacion = notacion # Simbolo o notacion que se esta midiendo
        self.color_linea = color # Color de la linea trazadora 

        # Acomodo de la ventana
        layout = QVBoxLayout()

        # Gráfica con matplotlib y canvas para renderizarla
        self.figura = Figure(figsize=(6,4))
        self.canvas = FigureCanvas(self.figura)
        self.ejes_grafica = self.figura.add_subplot(111)

        # Estilo del gráfico
        self.ejes_grafica.set_title(self.nombre_grafica, fontsize=10, color="white") # Etiqueta del titulo de la grafica
        self.ejes_grafica.set_xlabel(self.nombre_eje_x, fontsize=8, color="white") # Etiqueta del eje X
        self.ejes_grafica.set_ylabel(self.nombre_eje_y, fontsize=8, color="white") # Etiqueta del eje Y
        self.ejes_grafica.tick_params(axis="x", labelsize=7, rotation=45, color="white", labelcolor="white")
        self.ejes_grafica.tick_params(axis="y", labelsize=7, color="white", labelcolor="white") 
        self.ejes_grafica.grid(True, linestyle="--", alpha=0.5, color="white") # Cuadriculado de la vista 
        self.ejes_grafica.set_facecolor("#141924") # Fondo del area de la grafica
        self.figura.patch.set_facecolor("#141924") # Fondo exterior de la frafica
        self.linea_grafica = self.ejes_grafica.plot([], [], color=self.color_linea, linewidth=2)[0] # Linea trasadora de los datos
        self.etiquetas_valores = [] # Etiquetas de los datos sobre los puntos 

        # Añadiendo las etiquetas a la gráfica
        for _ in range(15):
            etiqueta = self.ejes_grafica.text(0, 0, "", fontsize=7, color="white", ha="center", va="bottom", visible=False)
            self.etiquetas_valores.append(etiqueta)

        # Agregar canvas de la gráfica al layout
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Etiqueta informativa para mostrar el último dato recibido
        self.info = QLabel("⏳ Esperando monitoreo...")
        self.info.setObjectName("EstiInfo") # Cambio de nombre al objeto para edicion en QSS
        layout.addWidget(self.info)

    # Método para agregar un dato a la gráfica
    def agregarDato(self, dato):
        dato = round(dato, 1)
        self.contador_segundos += 1

        # Agregar los datos a las listas temporales
        self.tiempos_ventana.append(self.contador_segundos)
        self.datos_ventana.append(dato)

        # Validar la cantidad de datos en la ventana de la gráfica
        if len(self.tiempos_ventana) > 15:
            self.tiempos_ventana.pop(0)
            self.datos_ventana.pop(0)
    
        self.actualizarGrafica()
        self.info.setText(f"📡 Último dato: {dato} {self.notacion}")

    # Método para actualizar la gráfica
    def actualizarGrafica(self):
        # 1. Actualizar los datos de la línea existente
        self.linea_grafica.set_data(self.tiempos_ventana, self.datos_ventana)

        # 2. Actualizar las etiquetas de texto (números sobre los puntos)
        for indice_punto, (x, y) in enumerate(zip(self.tiempos_ventana, self.datos_ventana)):
            if indice_punto < len(self.etiquetas_valores):
                self.etiquetas_valores[indice_punto].set_position((x, y))
                self.etiquetas_valores[indice_punto].set_text(f"{y}")
                self.etiquetas_valores[indice_punto].set_visible(True)
        # Ocultar las etiquetas restantes si hay menos de 15 puntos
        for indice_punto in range(len(self.tiempos_ventana), len(self.etiquetas_valores)):
            self.etiquetas_valores[indice_punto].set_visible(False)

        # 3. Reajustar los límites de los ejes automáticamente
        self.ejes_grafica.relim()
        self.ejes_grafica.autoscale_view()

        # 4. Forzar el reajuste del eje X para mantener la ventana de 15 puntos
        if len(self.tiempos_ventana) > 1:
            self.ejes_grafica.set_xlim(min(self.tiempos_ventana), max(self.tiempos_ventana))
        elif len(self.tiempos_ventana) == 1:
            x = self.tiempos_ventana[0]
            self.ejes_grafica.set_xlim(x - 1, x + 1)

        self.figura.tight_layout()
        # 5. Redibujar solo el canvas
        self.canvas.draw()

    #limpiar datos en ventana
    def limpiarVista(self):
        self.datos_ventana.clear()
        self.tiempos_ventana.clear()
        self.contador_segundos =0
        self.actualizarGrafica()
        self.info.setText("⏳ Esperando monitoreo...")
