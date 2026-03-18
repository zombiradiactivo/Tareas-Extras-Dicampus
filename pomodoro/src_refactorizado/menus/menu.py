from rich.panel import Panel
from rich.console import Console
from rich.prompt import IntPrompt, Confirm
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
