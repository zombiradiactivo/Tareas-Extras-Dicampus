from utils.enviar_notificacion import enviar_notificacion
from utils.temporizador import ejecutar_temporizador
from menus.menu import mostrar_menu
from rich.console import Console
console = Console()

def iniciar_pomodoro():
    # 1. Menú inicial y configuración
    t_trabajo, t_descanso = mostrar_menu()
    pomodoros_completados = 0

    try:
        while True:
            # 2. Sesión de Trabajo
            enviar_notificacion("¡A trabajar!", f"Sesión #{pomodoros_completados + 1}", "(P) Pausar/Reanudar (S) Salir")
            ejecutar_temporizador(t_trabajo, "Trabajando 🛠️", "green")
            
            pomodoros_completados += 1
            console.print(f"\n[bold gold1]✅ ¡Pomodoro #{pomodoros_completados} completado![/bold gold1]\n")

            # 3. Lógica de Descanso
            if pomodoros_completados % 4 == 0:
                enviar_notificacion("Descanso Largo", "15 minutos de relax.","(P) Pausar/Reanudar (S) Salir")
                ejecutar_temporizador(15 * 60, "Descanso Largo 🧘", "blue")
            else:
                enviar_notificacion("Descanso Corto", "5 minutos para estirar.","(P) Pausar/Reanudar (S) Salir")
                ejecutar_temporizador(t_descanso, "Descanso Corto ☕", "cyan")

    except KeyboardInterrupt:
        console.print(f"\n[bold red]Sesión finalizada.[/bold red] Total hoy: {pomodoros_completados} 🍅")

if __name__ == "__main__":
    iniciar_pomodoro()