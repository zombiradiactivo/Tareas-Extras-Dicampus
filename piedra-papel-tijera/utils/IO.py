
from utils.cli_menus import mostrar_menu
from utils.utils import obtener_opciones


def obtener_emoji(opcion):
    # Mapeo de emojis para las 15 variantes [cite: 1-16]
    emojis = {
        "Human": "👤", "Tree": "🌳", "Wolf": "🐺", "Sponge": "🧽", "Paper": "📄",
        "Air": "💨", "Water": "💧", "Dragon": "🐉", "Devil": "😈", "Lightning": "⚡",
        "Gun": "🔫", "Rock": "🪨", "Fire": "🔥", "Scissors": "✂️", "Snake": "🐍"
    }
    return emojis.get(opcion, "❓")


def capturar_eleccion_jugador():
    opciones = obtener_opciones()
    mostrar_menu(opciones)
    
    while True:
        try:
            seleccion = int(input("Introduce el número de tu elección: "))
            if 1 <= seleccion <= len(opciones):
                # Convertir el número introducido al nombre de la elección
                nombre_eleccion = opciones[seleccion - 1]
                print(f"Has elegido: {nombre_eleccion}")
                return nombre_eleccion
            else:
                print(f"Error: Por favor, elige un número entre 1 y {len(opciones)}.")
        except ValueError:
            print("Error: Entrada no válida. Introduce un número entero.")
