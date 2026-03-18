# Tarea: Permitir al usuario ajustar duración de trabajo y descanso
from src_refactorizado.utils.obtener_tiempos import obtener_valor_validado

# Tarea: Tiempos configurables (almacenados en variables)
TRABAJO_MIN = obtener_valor_validado("Duración del trabajo en minutos", 25)
DESCANSO_MIN = obtener_valor_validado("Duración del descanso en minutos", 5)

# Conversión a segundos para el motor de pomodoro.py
DURACION_TRABAJO = TRABAJO_MIN * 60
DURACION_DESCANSO = DESCANSO_MIN * 60

print(f"\n✅ Configuración guardada: {TRABAJO_MIN} min trabajo / {DESCANSO_MIN} min descanso.\n")