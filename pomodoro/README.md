# 🍅 Interactive Pomodoro Timer

Un temporizador interactivo desarrollado en Python diseñado para mejorar la productividad. Esta herramienta implementa la famosa Técnica Pomodoro, alternando bloques de trabajo enfocado con breves periodos de descanso para mantener la agilidad mental.
## ✨ Características

- Ciclo Estándar: Configurado con el método tradicional de 25 minutos de trabajo y 5 minutos de descanso.

- Interfaz Interactiva: Notificaciones claras sobre el cambio de estado (Trabajo/Descanso).

- Control de Flujo: Capacidad para iniciar, pausar o reiniciar el temporizador.

- Contador de Sesiones: Realiza un seguimiento de cuántos "pomodoros" has completado en tu jornada.

## 🚀 Instalación y Uso
Requisitos Previos

Asegúrate de tener instalado Python 3.x en tu sistema.
Configuración

Clona este repositorio:
````Bash
git clone https://github.com/zombiradiactivo/Tareas-Extras-Dicampus.git
````
Navega al directorio del proyecto:
````Bash
cd pomodoro
````
Ejecuta la aplicación:
````Bash
python pomodoro.py
````


## 🛠️ Cómo funciona la técnica

El flujo de trabajo que sigue esta aplicación es:

1. Trabajo (25 min): Concentración total en una sola tarea.

2. Descanso corto (5 min): Desconexión para recargar energías.

3. Repetición: Tras 4 pomodoros, se recomienda un descanso largo (15-30 min).

## 📂 Estructura del Proyecto

- pomodoro.py: Punto de entrada de la aplicación.

- notificaciones.py: Contiene el motor del temporizador y la gestión del tiempo.

- config.py: Contiene las configuraciones.