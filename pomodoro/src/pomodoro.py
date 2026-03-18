from config import DURACION_TRABAJO, DURACION_DESCANSO 
from notificaciones import enviar_notificacion 
import time

# Tarea: Definir duración de descanso largo (15 min)
DURACION_DESCANSO_LARGO = 15 * 60

def cuenta_regresiva(segundos, mensaje="Tiempo restante"):
    """Realiza la cuenta regresiva mostrando el tiempo en MM:SS."""
    while segundos >= 0:
        minutos, segs = divmod(segundos, 60)
        print(f"{mensaje}: {minutos:02d}:{segs:02d}", end="\r")
        time.sleep(1)
        segundos -= 1
    print("\n")

def mostrar_estadisticas(ciclos):
    """
    Tarea: Mostrar estadísticas al final de cada ciclo.
    """
    print("-" * 30)
    print(f"📊 ESTADÍSTICAS ACTUALES")
    print(f"✅ Pomodoros completados: {ciclos}")
    print(f"⏳ Próximo objetivo: {'Descanso Largo' if ciclos % 4 == 0 else 'Siguiente Pomodoro'}")
    print("-" * 30 + "\n")

def iniciar_pomodoro():
    """
    Controla el flujo de trabajo y descanso.
    """

    # Tarea: Contar cuántos pomodoros se han completado
    pomodoros_completados = 0

    try:
        while True:
# 1. Sesión de Trabajo
            print(f"🚀 Iniciando Pomodoro #{pomodoros_completados + 1}")
            enviar_notificacion("¡A trabajar!", f"Sesión #{pomodoros_completados + 1}")  
            cuenta_regresiva(DURACION_TRABAJO, "Trabajando")
            
            pomodoros_completados += 1
            mostrar_estadisticas(pomodoros_completados)

            # 2. Determinar tipo de descanso
            # Tarea: Implementar descanso largo cada 4 ciclos (15 min)
            if pomodoros_completados % 4 == 0:
                print("🧘 ¡Momento de un gran respiro! Descanso largo iniciado.")
                enviar_notificacion("Descanso Largo", "Te lo has ganado: 15 minutos.")  
                cuenta_regresiva(DURACION_DESCANSO_LARGO, "Descanso Largo")
            else:
                print("☕ Descanso corto iniciado.")
                enviar_notificacion("Descanso Corto", "Tómate 5 minutos.") 
                cuenta_regresiva(DURACION_DESCANSO, "Descanso Corto")
            
            print("🔔 ¡Descanso terminado! ¿Listo para el siguiente?\n")

    except KeyboardInterrupt:
        print(f"\n\n👋 Sesión finalizada. Total de pomodoros hoy: {pomodoros_completados}")

if __name__ == "__main__":
    iniciar_pomodoro()