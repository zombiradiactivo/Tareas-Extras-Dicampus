# 🎲 Simulador de Dados Interactivo

Un simulador de dados robusto basado en terminal, diseñado para entusiastas de los juegos de rol (RPG), juegos de mesa o cualquier persona que necesite generar azar con estadísticas detalladas.
## ✨ Características

    Variedad de Dados: Soporte para dados estándar de RPG: D4, D6, D8, D10, D12 y D20.

    Personalización Total: Elige cuántos dados lanzar y cuántas veces repetir la serie de lanzamientos.

    Estadísticas en Tiempo Real: Cálculo automático de la media, valor máximo, valor mínimo y suma total.

    Visualización de Datos: Gráficos de barras sencillos en texto para visualizar la distribución de los resultados directamente en la terminal.

    Persistencia: Opción para exportar el historial de tus tiradas a un archivo local.

    Historial de Sesión: Consulta tus lanzamientos previos sin salir del programa.

## 🚀 Instalación y Uso
1. Requisitos Previos

Asegúrate de tener instalado Python 3.x en tu sistema.
2. Clonar el repositorio
````Bash
git clone https://github.com/zombiradiactivo/Tareas-Extras-Dicampus.git
````
cd simulador-dados

3. Ejecutar el simulador
````Bash
python src/simulador.py
````

## 🛠️ Estructura del Proyecto

El proyecto sigue una estructura limpia y organizada:
````Plaintext

simulador-dados/
│
├── src/
│   └── simulador.py      # Lógica principal del simulador
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación (este archivo)
````
## 📊 Ejemplo de Salida
````Plaintext

--- Resultados de la Tirada (3d6) ---
Lanzamiento 1: [5, 2, 6] | Total: 13
Lanzamiento 2: [1, 4, 3] | Total: 8

--- Estadísticas Acumuladas ---
Mínimo: 1 | Máximo: 6 | Media: 3.5
Visualización:
6: ■■■■■ (1)
5: ■■■■■ (1)
...
````