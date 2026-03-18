from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
import msvcrt # Para Windows. En Unix usaría select/termios
import time
import sys

console = Console()

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
