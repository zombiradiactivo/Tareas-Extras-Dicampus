from config import DURACION_TRABAJO, DURACION_DESCANSO 
from notificaciones import enviar_notificacion 
import msvcrt  # Nota: Esta implementación es para Windows.
import time
import sys

# Tarea: Definir duración de descanso largo (15 min)
DURACION_DESCANSO_LARGO = 15 * 60

def cuenta_regresiva(segundos, mensaje="Trabajando"):
    """
    Tarea: Permitir pausar, reanudar y mostrar estado actual.
    """
    pausado = False
    
    while segundos >= 0:
        # Tarea: Mostrar estado actual (corriendo / pausado)
        estado = "[ PAUSADO ]" if pausado else "[ CORRIENDO ]"
        minutos, segs = divmod(segundos, 60)
        
        # Interfaz de terminal
        sys.stdout.write(f"\r{estado} {mensaje}: {minutos:02d}:{segs:02d} | (P) Pausar/Reanudar (S) Salir ")
        sys.stdout.flush()

        # Tarea: Detectar si se presionó una tecla
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode().lower()
            if tecla == 'p':
                pausado = not pausado
                print(f"\n{'▶️ Reanudando...' if not pausado else '⏸️ Temporizador en pausa.'}")
            elif tecla == 's':
                print("\nTerminando sesión...")
                sys.exit()

        if not pausado:
            time.sleep(1)
            segundos -= 1
        else:
            time.sleep(0.1) # Reducir carga de CPU mientras está pausado
            
    print("\n¡Tiempo completado!")

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
    pomodoros_completados = 0
    try:
        while True:
            # Sesión de Trabajo
            enviar_notificacion("¡A trabajar!", f"Sesión #{pomodoros_completados + 1}")
            cuenta_regresiva(DURACION_TRABAJO, "Trabajando")
            
            pomodoros_completados += 1
            
            # Lógica de descansos (largo cada 4)
            if pomodoros_completados % 4 == 0:
                enviar_notificacion("Descanso Largo", "15 minutos de relax.")
                cuenta_regresiva(15 * 60, "Descanso Largo")
            else:
                enviar_notificacion("Descanso Corto", "5 minutos para estirar.")
                cuenta_regresiva(DURACION_DESCANSO, "Descanso Corto")

    except KeyboardInterrupt:
        print(f"\nSesión finalizada. Pomodoros totales: {pomodoros_completados}")

if __name__ == "__main__":
    iniciar_pomodoro()