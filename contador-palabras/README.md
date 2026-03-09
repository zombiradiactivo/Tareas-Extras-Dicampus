# 📝 Contador de Palabras

Este programa permite obtener estadísticas detalladas tanto de entradas directas por consola como de archivos de texto, facilitando el procesamiento de datos textuales.

## ✨ Características

- Entrada Versátil: Soporta introducción de texto manual o lectura de archivos .txt.

- Análisis Detallado: Calcula el número total de palabras, caracteres, líneas y frecuencia de términos.

- Exportación de Resultados: Opción para guardar el informe generado en un archivo de salida.

- Interfaz Intuitiva: Menú sencillo directamente en la terminal.

## 📁 Estructura del Proyecto

```
contador-palabras/
│
├── README.md               # Documentación principal
├── .gitignore              # Archivos excluidos de Git
├── requirements.txt        # Dependencias del proyecto
├── src/
│   └── contador.py         # Lógica principal del programa
├── textos/
│   └── ejemplo.txt         # Archivo de ejemplo para pruebas
└── docs/
    └── asistencia_ia.md    # Registro de prompts y ayuda de IA
```
## 🚀 Instalación y Uso
### 1. Clonar el repositorio
```Bash
git clone https://github.com/zombiradiactivo/Tareas-Extras-Dicampus.git
cd contador-palabras
```
### 2. Instalar dependencias

Si el proyecto utiliza librerías externas (especificadas en requirements.txt):
````Bash
pip install -r requirements.txt
````
### 3. Ejecutar la aplicación

Para iniciar el analizador, ejecuta el script principal desde la raíz:
````Bash
python src/contador.py
````
## 📊 Ejemplo de Funcionamiento

Al ejecutar el programa, podrás elegir entre:

    Modo Manual: Escribes el texto y recibes el conteo al instante.

    Modo Archivo: Proporcionas la ruta (ej. textos/ejemplo.txt) y el sistema procesará el contenido automáticamente.

    Nota: El programa limpia automáticamente signos de puntuación comunes para asegurar que el conteo de palabras sea preciso.

## 🛠️ Tecnologías utilizadas

    Lenguaje: Python 3.x

    Librerías: os, sys (estándar de Python)