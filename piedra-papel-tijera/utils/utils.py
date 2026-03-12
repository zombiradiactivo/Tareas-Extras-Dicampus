import os
import random
from utils.variables import REGLAS as reglas

def limpiar_pantalla():
    # Limpia la terminal según el sistema operativo (Windows o Unix/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')



def obtener_opciones():
    # Lista de opciones basada en el orden de las reglas proporcionadas
    return [
        "Human", "Tree", "Wolf", "Sponge", "Paper", 
        "Air", "Water", "Dragon", "Devil", "Lightning", 
        "Gun", "Rock", "Fire", "Scissors", "Snake"
    ]

def determinar_ganador(jugador, computadora):
    # Diccionario basado en las reglas de Nivel 2 [cite: 1-16]

    if jugador == computadora:
        print(f"¡Empate! Ambos eligieron {jugador}.")
        return "Empate"
    
    # Verificamos si la elección de la computadora está en la lista de derrotados por el jugador
    if computadora in reglas[jugador]:
        print(f"¡Victoria! {jugador} vence a {computadora}.")
        return "Victoria"
    else:
        print(f"Derrota... {computadora} vence a {jugador}.")
        return "Derrota"

def generar_eleccion_computadora(opciones):
    """
    Selecciona un elemento aleatorio de la lista de opciones.
    """
    eleccion_ia = random.choice(opciones)
    print(f"\n🤖 La computadora ha elegido: {eleccion_ia}")
    return eleccion_ia
