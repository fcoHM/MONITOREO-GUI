from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import os

class Visual3D(QWidget):
    def __init__(self, rutaStl):
        super().__init__()

        self.actor = None
        self.rutaSTL = rutaStl

        # Historial de rotaciones para cada eje
        self.x_hist = []  # Historial de rotación eje X
        self.y_hist = []  # Historial de rotación eje Y
        self.z_hist = []  # Historial de rotación eje Z

        # Layout principal vertical
        self.layout = QVBoxLayout()
        self.iniciarVTK()  # Inicializa el widget VTK y el renderer

        # Etiqueta informativa para mostrar la orientación actual
        self.infoModel = QLabel("X: -00.00   Y: -00.00   Z: -00.00  ")
        self.infoModel.setObjectName("EstiInfo")
        self.layout.addWidget(self.infoModel)
        
        # Carga el modelo STL y ajusta la vista
        self.cargarSTL(self.rutaSTL)
        self.setZoomFijo(1300)
        self.setLayout(self.layout)

    def iniciarVTK(self):#inicializa el widget VTK y el renderer
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(20/255, 25/255, 36/255)  # Color de fondo oscuro
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.Disable()  # Deshabilita la interacción del usuario
        self.vtk_widget.setEnabled(False)

    def cargarSTL(self, ruta): # Carga un archivo STL y lo centra en el origen
        if not os.path.isfile(ruta):
            self.infoModel.setText("Archivo STL no encontrado.")
            return
        try:
            if self.actor:
                self.renderer.RemoveActor(self.actor)
            reader = vtk.vtkSTLReader()
            reader.SetFileName(ruta)
            reader.Update()
            polydata = reader.GetOutput()
            self.centrarOrigen(polydata)  # Centra el modelo en el origen
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydata)
            self.actor = vtk.vtkActor()
            self.actor.SetMapper(mapper)
            self.renderer.AddActor(self.actor)
            self.vtk_widget.GetRenderWindow().Render()
        except Exception as e:
            self.infoModel.setText(f"Error al cargar STL: {e}")

    def centrarOrigen(self, polydata): # Centra el modelo STL en el origen de coordenadas
        center = polydata.GetCenter()
        offset_y = 30  # Ajuste vertical opcional
        transform = vtk.vtkTransform()
        transform.Translate(-center[0], -center[1] - offset_y, -center[2])
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputData(polydata)
        transformFilter.SetTransform(transform)
        transformFilter.Update()
        polydata.ShallowCopy(transformFilter.GetOutput())

    def setZoomFijo(self, distancia): # Coloca la cámara a una distancia fija del modelo
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, distancia)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 1, 0)
        self.renderer.ResetCameraClippingRange()
        self.vtk_widget.GetRenderWindow().Render()

    def actualizarOrientacion(self, x: int, y: int, z: int): # Actualiza la orientación del modelo 3D y muestra los valores en la etiqueta. guarda el historial de rotaciones.
        if self.actor:
            if self.actor.GetOrientation() != (x, y, z): # Compara la orientacion con la anteror de que no sea igual
                self.actor.SetOrientation(x, y, z)
                self.renderer.ResetCameraClippingRange()
                self.vtk_widget.GetRenderWindow().Render()
        self.infoModel.setText(f"X: {x}  Y: {y}  Z: {z}   ")
        self.x_hist.append(x)
        self.y_hist.append(y)
        self.z_hist.append(z)

    # Métodos get para los historiales de rotación
    def getX_hist(self):
        return self.x_hist
    
    def getY_hist(self):
        return self.y_hist

    def getZ_hist(self):
        return self.z_hist

    def cambiarModelo3D(self, nueva_ruta_stl):
        if self.rutaSTL != nueva_ruta_stl and nueva_ruta_stl:
            self.rutaSTL = nueva_ruta_stl
            self.cargarSTL(self.rutaSTL)

    def limpiarVista(self):
        # limpia los historiales de datos
        self.x_hist.clear()
        self.y_hist.clear()
        self.z_hist.clear()

        # restablece la etiqueta de información
        self.infoModel.setText("X: -00.00   Y: -00.00   Z: -00.00  ")

        # restablece la orientación del modelo 3D a su estado inicial (0, 0, 0)
        if self.actor:
            self.actor.SetOrientation(0, 0, 0)
            self.vtk_widget.GetRenderWindow().Render()