from config import DURACION_TRABAJO, DURACION_DESCANSO # No implementado todavia
## from notificaciones import enviar_notificacion # No implementado todavia
import time

def cuenta_regresiva(segundos, mensaje="Tiempo restante"):
    """Realiza la cuenta regresiva mostrando el tiempo en MM:SS."""
    while segundos >= 0:
        minutos, segs = divmod(segundos, 60)
        print(f"{mensaje}: {minutos:02d}:{segs:02d}", end="\r")
        time.sleep(1)
        segundos -= 1
    print("\n")

def iniciar_pomodoro():
    """
    Controla el flujo de trabajo y descanso.
    """
    # Tarea: Implementar sesión de trabajo (25 min = 1500 seg)
    print("--- 🛠️ SESIÓN DE TRABAJO INICIADA ---")
    print("¡A trabajar!", "Es momento de concentrarse.")
    cuenta_regresiva(DURACION_TRABAJO, "Trabajando")

    # Tarea: Notificar cambio de sesión
    print("--- ☕ HORA DE DESCANSAR ---")
    print("¡Descanso!", "Tómate un respiro de 5 minutos.")

    # Tarea: Implementar sesión de descanso (5 min = 300 seg)
    cuenta_regresiva(DURACION_DESCANSO, "Descansando")
    
    print("--- ✅ CICLO COMPLETADO ---")
    print("Ciclo terminado", "¿Listo para el siguiente?")

if __name__ == "__main__":
    iniciar_pomodoro()