import os

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo (Windows o Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    """Muestra el banner principal del programa con estilo visual."""
    limpiar_pantalla()
    print("="*55)
    print("      🛡️  GENERADOR DE CONTRASEÑAS  🛡️")
    print("="*55)
