from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraficaMaximo(QWidget):
    def __init__(self, nombre_grafica, nomX, nomY, notacion, color):
        super().__init__() # se manda a llamar a la clase padre para la constricion de la ventana/componente
        self.setMinimumSize(480, 370)  # Tamaño inicial de la ventana QT

        # atributos del compente
        self.contador_segundos = 0 # Segundos de la grafica
        self.nombre_grafica = nombre_grafica  # Nombre de la grafica
        self.nombre_eje_x = nomX # Nombre del eje X
        self.nombre_eje_y = nomY # Nombre del eje Y
        self.notacion = notacion # Simbolo o notacion que se esta midiendo
        self.color_linea = color # Color de la linea trazadora 

        #contenedor de los datos llegados
        self.datos_ventana = []
        self.tiempos_ventana =[]
        self.maximo = 0

        # acomodo de la ventana
        layout = QVBoxLayout()

        # grafica con matplotlib  y canvas  para renderizarla
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
        
        #etiqueta dentro del grafico que muestra el darto maximo llegado 
        self.etiqueta_maximo = self.ejes_grafica.annotate(
            "", 
            xy=(0, 0), 
            xytext=(0, -25), 
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color=self.color_linea),
            ha='center', 
            va='top',
            fontsize=8,
            color = self.color_linea,
            bbox=dict(boxstyle="round,pad=0.3", fc="black", ec=self.color_linea, lw=1, alpha=0.7)
        )
        self.etiqueta_maximo.set_visible(False)
        self.setLayout(layout)

        # Agregar canvas de la gráfica al layout
        layout.addWidget(self.canvas)
        # Etiqueta informativa para mostrar el último dato recibido
        self.info = QLabel("⏳ Esperando monitoreo...")
        self.info.setObjectName("EstiInfo") # Cambio de nombre al objeto para edicion en QSS
        # Etiqueta para el dato maximo llegado 
        self.infoMaximo = QLabel("Maximo: 00.00")
        self.infoMaximo.setObjectName("EstiInfo")

        layout.addWidget(self.info)
        layout.addWidget(self.infoMaximo)

    # agregar un dato nuevo a la grafica 
    def agregarDato(self, dato):
        dato = int(dato)
        self.contador_segundos += 1 # agregamos 1

        self.datos_ventana.append(dato)# se agrega el nuevo dato
        self.tiempos_ventana.append(self.contador_segundos)# se agrega el nuevo segundo
        # ver si hay un nuevo maximo
        if self.datos_ventana:
            maximo_actual = max(self.datos_ventana)
            if maximo_actual > self.maximo:
                self.maximo = maximo_actual
        
         # Validar la cantidad de datos en la ventana de la gráfica
        if len(self.tiempos_ventana) > 50:
            self.tiempos_ventana.pop(0)
            self.datos_ventana.pop(0)

        self.actualizarGrafica()
        self.info.setText(f"📡 Último dato: {dato} {self.notacion}")
        self.infoMaximo.setText(f"Maximo: {self.maximo} {self.notacion}")


    def actualizarGrafica(self):
        #1. Actualizar los datos de la línea existente
        self.linea_grafica.set_data(self.tiempos_ventana, self.datos_ventana)

        #2. Reajustar los límites de los ejes automáticamente
        self.ejes_grafica.relim()
        self.ejes_grafica.autoscale_view()

        #3. Forzar el reajuste del eje X para mantener la ventana de 15 puntos
        if len(self.tiempos_ventana) > 1:
            self.ejes_grafica.set_xlim(min(self.tiempos_ventana), max(self.tiempos_ventana))
        elif len(self.tiempos_ventana) == 1:
            x = self.tiempos_ventana[0]
            self.ejes_grafica.set_xlim(x - 1, x + 1)
        
        self.actualizarEtiquetaMaximo()

        self.figura.tight_layout()
        #4. Redibujar solo el canvas
        self.canvas.draw()

    def actualizarEtiquetaMaximo(self):
        if not self.datos_ventana:
            self.etiqueta_maximo.set_visible(False)
            return

        maximo_valor = -float('inf')
        max_x = 0
        
        # Encontrar el valor máximo y su correspondiente tiempo en la ventana actual
        for i in range(len(self.datos_ventana)):
            if self.datos_ventana[i] > maximo_valor:
                maximo_valor = self.datos_ventana[i]
                max_x = self.tiempos_ventana[i]

        # Actualizar la posición y texto de la etiqueta
        self.etiqueta_maximo.xy = (max_x, maximo_valor)
        self.etiqueta_maximo.set_text(f"Max: {maximo_valor:.2f}")
        self.etiqueta_maximo.set_visible(True)
    

    #limpiar datos en ventana
    def limpiarVista(self):
        self.datos_ventana.clear()
        self.tiempos_ventana.clear()
        self.actualizarGrafica()
        self.contador_segundos = 0
        self.info.setText("⏳ Esperando monitoreo...")
        self.infoMaximo.setText("Maximo: 00.00")

    def obtenerMaximo(self):
        return max(self.datos_ventana)

     # Métodos get para las listas
    def getDatos(self):
        return self.datos_historial