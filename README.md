# 🚀 Interfaz Gráfica para CANSAT

Este proyecto es una interfaz gráfica desarrollada con **PySide6**, diseñada para visualizar en tiempo real los datos transmitidos por un satélite tipo **CANSAT**.

Se enfoca en representar parámetros como:

- 🌡️ **Temperatura**
- 📈 **Presión**
- 🛰️ **Altura**

Proporcionando una herramienta clara y eficiente para el monitoreo durante el vuelo y la fase de pruebas.

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

## ⚙️ Configuración del Entorno Virtual

### 1️⃣ Crear el entorno virtual

```bash
# En Windows
python -m venv env
env\Scripts\activate.bat

# En Linux o MacOS
python3 -m venv env
source env/bin/activate

# Instalar dependencias
pip install PySide6 vtk pyserial pandas matplotlib numpy

# Enpaquetado en .exe
pyinstaller --onefile --windowed --name "MONITOREO_GUI" --icon="Media/icono.ico" --exclude-module PyQt6 --exclude-module PyQt5 --add-data "View/Styles;View/Styles" --add-data "Media/Model3D;Media/Model3D" --add-data "View/Components/Mapas;View/Components/Mapas" --hidden-import "PySide6.QtLocation" --hidden-import "PySide6.QtPositioning" main.py 
