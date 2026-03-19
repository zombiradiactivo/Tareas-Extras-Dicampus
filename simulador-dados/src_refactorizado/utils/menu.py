import os


def limpiar_pantalla():
    """
    Limpia la terminal de comandos según el sistema operativo actual.
    
    Utiliza 'cls' para sistemas Windows (nt) y 'clear' para sistemas 
    basados en Unix (Linux/macOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    """
    Imprime en pantalla el encabezado visual del programa.
    
    Muestra el título del simulador y los tipos de dados soportados
    dentro de un marco decorativo.
    """
    print("==========================================")
    print("🎲  BIENVENIDO AL SIMULADOR DE DADOS  🎲")
    print("      (D4, D6, D8, D10, D12, D20)       ")
    print("==========================================\n")
