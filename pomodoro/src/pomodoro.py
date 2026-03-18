import sys
import time
import msvcrt # Para Windows. En Unix usaría select/termios
from rich.panel import Panel
from rich.console import Console
from rich.prompt import IntPrompt, Confirm
from notificaciones import enviar_notificacion
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

def mostrar_menu():
    """
    Tarea: Crear menú interactivo al iniciar la aplicación (usando rich).
    Tarea: Capturar entrada del usuario para configurar sesión.
    """
    console.clear()
    console.print(Panel.fit(
        "[bold tomato]🍅 BIENVENIDO AL TEMPORIZADOR POMODORO[/bold tomato]\n"
        "[white]Gestiona tu tiempo de forma eficiente.[/white]",
        border_style="green"
    ))

    # Captura de datos con validación integrada de Rich
    trabajo = IntPrompt.ask("Minutos de [bold green]TRABAJO[/bold green]", default=25)
    descanso = IntPrompt.ask("Minutos de [bold blue]DESCANSO[/bold blue]", default=5)
    
    confirmar = Confirm.ask("¿Deseas comenzar la sesión ahora?")
    
    if not confirmar:
        console.print("[yellow]Sesión cancelada. ¡Hasta pronto![/yellow]")
        exit()
        
    return trabajo * 60, descanso * 60

def ejecutar_temporizador(segundos, tarea, color):
    """
    Ejecuta la barra de progreso permitiendo pausa (P) y salida (S).
    """
    pausado = False
    
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console,
        transient=True # Limpia la barra al terminar
    ) as progress:
        
        task = progress.add_task(f"[{color}]{tarea}", total=segundos)
        
        while not progress.finished:
            # Tarea: Detectar pulsación de tecla para pausa/reanudación
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode().lower()
                if tecla == 'p':
                    pausado = not pausado
                    nuevo_estado = f"[bold yellow]PAUSADO[/] {tarea}" if pausado else f"[{color}]{tarea}"
                    progress.update(task, description=nuevo_estado)
                elif tecla == 's':
                    console.print("[bold red]\nSesión cancelada por el usuario.[/]")
                    sys.exit()

            if not pausado:
                time.sleep(1)
                progress.update(task, advance=1)
            else:
                time.sleep(0.1) # Evita consumo excesivo de CPU en pausa

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