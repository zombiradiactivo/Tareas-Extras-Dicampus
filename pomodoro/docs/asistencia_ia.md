Prompt 1

Genera el README.md del siguiente proyecto 

Este proyecto consiste en desarrollar en python un temporizador Pomodoro interactivo que permita alos usuarios gestionar su tiempo de trabajo y descanso usando la técnica Pomodoro (25 mintrabajo / 5 min descanso). 

Prompt 2

La estructura es la siguiente 
C:.
└───src
        config.py
        notificaciones.py
        pomodoro.py

Completa solo lo que se pide en cada tarea 

Archivo: src/pomodoro.py
Tareas:
• Crear función que haga cuenta regresiva en segundos
• Mostrar el tiempo restante en terminal (MM:SS)
• Probar manualmente con 1 minuto

Prompt 3

Archivo: src/pomodoro.py
Tareas:
• Implementar sesión de trabajo de 25 minutos
• Implementar sesión de descanso de 5 minutos
• Notificar al usuario cuando cambia la sesión

Prompt 4

Archivo: src/config.py
Tareas:
• Crear archivo config.py con tiempos configurables
• Permitir al usuario ajustar duración de trabajo y descanso
• Validar que los valores sean positivos

Prompt 5 

Archivo: src/pomodoro.py
Tareas:
• Contar cuántos pomodoros se han completado
• Implementar descanso largo cada 4 ciclos (15 min)
• Mostrar estadísticas al final de cada ciclo

Prompt 6 

Archivo: src/notificaciones.py
Tareas:
• Emitir sonido al terminar cada sesión (beep de terminal)
• Mostrar mensaje visual destacado al cambiar de sesión
• Manejar sistemas operativos diferentes (Windows/Linux/Mac)