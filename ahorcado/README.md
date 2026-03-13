# Juego del Ahorcado

¡Bienvenido al Juego del Ahorcado! Esta es una versión interactiva del clásico juego de adivinanzas, potenciada con una base de datos SQLite para gestionar un diccionario dinámico de palabras.
## 📝 Descripción del Proyecto

El objetivo principal es adivinar una palabra oculta letra por letra antes de que el "ahorcado" sea completado (agotar los intentos). A diferencia de las versiones estáticas, este proyecto integra persistencia de datos, permitiendo que el vocabulario crezca y se gestione de forma eficiente.
Características Principales:

- Mecánica Clásica: Sistema de intentos limitados y visualización de - progreso.

- Diccionario Persistente: Uso de SQLite para almacenar y recuperar - palabras.
 
- Gestión de Palabras: Interfaz o funciones para consultar el - catálogo actual y añadir nuevos retos a la base de datos.
 
- Selección Aleatoria: El sistema elige una palabra al azar de la - base de datos en cada partida.

## 🚀 Instalación y Uso

Clonar el repositorio:
```Bash
git clone https://github.com/zombiradiactivo/Tareas-Extras-Dicampus.git
```
Preparar la Base de Datos:

Asegúrate de tener SQLite instalado. Al iniciar la aplicación porprimera vez, se creará automáticamente el archivo .db con la tablade palabras (o puedes ejecutar el script de inicializaciónincluido).

Ejecutar la aplicación (2 versiones):

version 1
````Bash
python src/base/ahorcado.py
````
version 2
```Bash
python main.py
```
## 🛠️ Tecnologías Utilizadas

    Lenguaje:  Python

    Base de Datos: SQLite 3

    Interfaz:   Consola (CLI)

## 📊 Estructura de la Base de Datos

La base de datos cuenta con una tabla principal llamada palabras:

|Campo |    Tipo |      Descripción |
|-|         -|          -|
|id |       INTEGER|    Clave primaria autoincremental.|
|palabra|   TEXT|       La palabra a adivinar (en mayúsculas).|
|pista|     TEXT|       (Opcional) Una breve ayuda para el jugador.|