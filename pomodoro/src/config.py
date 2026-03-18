import sys

def obtener_valor_validado(mensaje, default):
    """
    Tarea: Validar que los valores sean positivos y numéricos.
    """
    while True:
        entrada = input(f"{mensaje} (Presiona Enter para usar {default} min): ")
        if not entrada:
            return default
        
        try:
            valor = int(entrada)
            if valor > 0:
                return valor
            else:
                print("❌ El valor debe ser un número positivo (mayor a 0).")
        except ValueError:
            print("❌ Entrada no válida. Por favor, introduce un número entero.")

# Tarea: Permitir al usuario ajustar duración de trabajo y descanso
print("--- ⚙️ CONFIGURACIÓN DEL TEMPORIZADOR ---")

# Tarea: Tiempos configurables (almacenados en variables)
TRABAJO_MIN = obtener_valor_validado("Duración del trabajo en minutos", 25)
DESCANSO_MIN = obtener_valor_validado("Duración del descanso en minutos", 5)

# Conversión a segundos para el motor de pomodoro.py
DURACION_TRABAJO = TRABAJO_MIN * 60
DURACION_DESCANSO = DESCANSO_MIN * 60

print(f"\n✅ Configuración guardada: {TRABAJO_MIN} min trabajo / {DESCANSO_MIN} min descanso.\n")