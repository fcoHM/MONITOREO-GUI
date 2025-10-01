import QtQuick 2.15
import QtLocation 5.15
import QtPositioning 5.15

// Item es el contenedor base para los elementos visuales en QML.
Item {
    anchors.fill: parent // ocupa el mismo ancho de la ventana padre

    
    Plugin {
        id: mapPlugin
        name: "osm" // "osm" se refiere a OpenStreetMap.
        PluginParameter { name: "osm.mapping.host"; value: "https://tile.openstreetmap.org/%z/%x/%y.png" }
    }

    // --- El componente del Mapa ---
    Map {
        id: mapa
        anchors.fill: parent
        plugin: mapPlugin // Le dice al mapa que use el plugin que definimos arriba.
        zoomLevel: 14 // Nivel de zoom inicial.

        // Coordenada inicial donde se centrará el mapa al arrancar.
        center: QtPositioning.coordinate(22.15, -102.3)

        // --- Marcador en el mapa ---
        MapQuickItem {
            id: marcador
            // Coordenada inicial del marcador.
            coordinate: QtPositioning.coordinate(22.15, -102.3)
            
            // tamanio de icono
            anchorPoint.x: icon.width / 2
            anchorPoint.y: icon.height

            // sourceItem define la apariencia visual del marcador.
            sourceItem: Image {
                id: icon
                source: "https://cdn-icons-png.flaticon.com/512/684/684908.png" // URL del icono.
                width: 32
                height: 32
            }
        }

        // comecion con las senales del back-and
        Connections {
            // 'target: gps' le dice que escuche al objeto "gps" que expusimos desde Python.
            target: gps
            // Esta función se ejecuta AUTOMÁTICAMENTE cada vez que el objeto 'gps' en Python
            // El nombre de la función debe ser 'on' + el nombre de la señal (en formato camelCase).
            function onCoordenadas_actualizadas(lat, lon) {
                marcador.coordinate = QtPositioning.coordinate(lat, lon)
                mapa.center = marcador.coordinate
            }

            function onSignalZoom(zoom) {
                mapa.zoomLevel = zoom
            }
        }
    }
}

