# 🚀 Interfaz de Monitoreo para Cohetes y Satélites

Este proyecto es una interfaz gráfica desarrollada con **PySide6**, diseñada para visualizar en tiempo real los datos transmitidos por sistemas de **cohetería experimental** y satélites tipo **CANSAT**.  

Su propósito es representar de manera clara la información recibida durante el vuelo o en fase de pruebas, ya sea proveniente de un **cohete** o de un **satélite**, dependiendo de lo que se esté monitoreando en ese momento.  

Entre los parámetros que se pueden visualizar se incluyen:  

- 🌡️ **Temperatura**  
- 📈 **Presión**  
- 🛰️ **Altura**  
- 📡 **Telemetría general del vuelo**  

De esta forma, la herramienta se convierte en un apoyo esencial para la interpretación y análisis de datos en proyectos aeroespaciales estudiantiles.
[🎥 Ver video del System Monitoring](Media/imagenes/SystemMonitoring.mp4)

---

## 🧩 Arquitectura del Proyecto

El sistema está basado en el patrón de diseño **MVC (Modelo - Vista - Controlador)**, lo cual permite:  

- 🧼 Separación clara de responsabilidades  
- 📦 Organización modular con clases orientadas a objetos  
- 🎨 Estilos visuales personalizables con hojas `.qss`  
- 🖼️ Vistas independientes por funcionalidad  
- 🔗 Fácil integración con otros sistemas  

Este enfoque ofrece una experiencia visual limpia, escalable y adaptable a las necesidades futuras del equipo.  

---

## 📚 Librerías y Versiones

Este proyecto depende de las siguientes librerías principales. Las versiones listadas son las que se han utilizado durante el desarrollo y se ha verificado su compatibilidad.

- **PySide6**: `6.9.1`
- **matplotlib**: `3.10.3`
- **pyserial**: `3.5`
- **vtk**: `9.5.0`

---

## ⚙️ Configuración del Entorno Virtual

### 1️⃣ Crear el entorno virtual

```bash
# En Windows
python -m venv env
env\Scripts\activate.bat

# En Linux o MacOS
python3 -m venv env
source env/bin/activate
```

### 2️⃣ Instalar Dependencias

Para instalar todas las dependencias necesarias, ejecuta el siguiente comando después de activar tu entorno virtual:

```bash
pip install PySide6 vtk pyserial pandas matplotlib numpy
```

---

## 📦 Empaquetado

Para generar un archivo ejecutable `.exe` del proyecto, puedes usar `pyinstaller` con la siguiente configuración:

```bash
pyinstaller --onefile --windowed --name "MONITOREO_GUI" --icon="Media/icono.ico" --exclude-module PyQt6 --exclude-module PyQt5 --add-data "View/Styles;View/Styles" --add-data "Media/Model3D;Media/Model3D" --add-data "View/Components/Mapas;View/Components/Mapas" --add-data "Media/marcador_ubi.ico;Media" --hidden-import "PySide6.QtLocation" --hidden-import "PySide6.QtPositioning" main.py
```
