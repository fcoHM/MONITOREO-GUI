import QtQuick 2.15
import QtLocation 5.15
import QtPositioning 5.15

Item {
    anchors.fill: parent

    Plugin {
        id: mapPlugin
        name: "osm"
        
        // Configuración específica para OpenStreetMap
        PluginParameter { 
            name: "osm.mapping.providersrepository.disabled"
            value: "true" // Deshabilita los proveedores por defecto
        }
        PluginParameter {
            name: "osm.mapping.offline.directory"
            value: "C:/CANSAT-GUI/Media/OfflineMapTiles"
        }
        PluginParameter { 
            name: "osm.mapping.custom.host"
            value: "https://tile.openstreetmap.org/" 
        }
        PluginParameter { 
            name: "osm.mapping.host"
            value: "https://tile.openstreetmap.org/" 
        }
        PluginParameter { 
            name: "osm.useragent"
            value: "MyQtApp/1.0 (+https://mi-dominio.com; contact: mi-email@dominio.com)"
        }
        PluginParameter { 
            name: "osm.mapping.cache.directory"
            value: "C:/CANSAT-GUI/Media/OfflineMapTiles" 
        }
        
    }

    Map {
        id: mapa
        anchors.fill: parent
        plugin: mapPlugin
        zoomLevel: 14
        center: QtPositioning.coordinate(22.785777844047804, -102.61300693209539)

        // cordenadas del CREDES 22.785777844047804, -102.61300693209539
        MapQuickItem {
            id: marcador
            coordinate: QtPositioning.coordinate(22.785777844047804, -102.61300693209539)
            anchorPoint.x: icon.width / 2
            anchorPoint.y: icon.height

            sourceItem: Image {
                id: icon
                source: iconPath // Use the iconPath from the QML context
                width: 28
                height: 28
            }
        }

        Connections {
            target: gps
            
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