# Analizador de Datos de Netflix 🎬

Una herramienta de escritorio desarrollada en Python que permite cargar, limpiar, analizar y visualizar conjuntos de datos de Netflix (archivos CSV). La aplicación utiliza una interfaz gráfica intuitiva para facilitar el flujo de trabajo de Ciencia de Datos, desde la detección de valores nulos hasta la generación de gráficos estadísticos.
## 🚀 Características

La aplicación está dividida en módulos funcionales accesibles mediante una interfaz de pestañas:

- Gestión de Datos: Carga de archivos CSV y vista preliminar de crudo.

- Limpieza Automática: * Tratamiento de valores nulos (especialmente en director, cast y country).

    - Eliminación de duplicados.

    - Normalización de formatos de texto y fechas.

    - Extracción de datos numéricos (conversión de duraciones a minutos).

- Análisis Estadístico: Cálculo de media, desviación estándar y percentiles utilizando NumPy.

- Visualizaciones Dinámicas: * 

    - Tarea 1: Histórico de títulos añadidos por año.

    - Tarea 2: Comparativa "Películas vs Series" y Top 10 de países productores.

    - Tarea 3: Evolución temporal de lanzamientos con anotaciones de picos máximos.

    - Tarea 4: Top 10 de géneros más populares con métricas detalladas.

## 🛠️ Tecnologías Utilizadas

- Python 3.x

- Tkinter: Para la interfaz gráfica de usuario (GUI).

- Pandas: Para la manipulación y estructuración de los datos.

- NumPy: Para el procesamiento de cálculos estadísticos avanzados.

- Matplotlib: Para la generación de gráficos y visualizaciones.

## 📋 Requisitos Previos

Asegúrate de tener instaladas las dependencias necesarias antes de ejecutar la aplicación:
````Bash
pip install pandas numpy matplotlib
````
## 📂 Estructura del Proyecto
````Plaintext
.
├── src
|    analisis_netflix.py   # Archivo principal de la aplicación
└── data/                 # Carpeta para los archivos CSV
    netflix_titles.csv
````
## 📖 Modo de Uso

Ejecución: Inicia el script principal:
````Bash
python analisis_netflix.py
````

- Carga: Haz clic en el botón "Cargar CSV" y selecciona tu dataset de Netflix.

- Exploración: Usa "Mostrar Información" o "Detectar Nulos" para entender eestado inicial de tus datos.

- Procesamiento: Presiona "Limpiar Datos". Este paso es fundamental parhabilitar las pestañas de estadísticas y visualizaciones.

- Visualización: Dirígete a la pestaña de "Visualizaciones" y navega entre la"Tareas" para ver los gráficos generados.

## 📊 Ejemplo de Visualizaciones Incluidas

La aplicación genera gráficos integrados en la interfaz de usuario, tales como:

- Gráficos de Barras: Para distribución anual y de géneros.

- Gráficos de Pastel: Para la proporción entre películas y series.

- Gráficos de Líneas: Para observar tendencias de lanzamiento a lo largo de las décadas.