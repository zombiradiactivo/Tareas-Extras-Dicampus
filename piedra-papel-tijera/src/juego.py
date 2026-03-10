import random

# 1. Inicialización de variables (Marcador)
victorias = 0
derrotas = 0
empates = 0

def obtener_opciones():
    # Lista de opciones basada en el orden de las reglas proporcionadas
    return [
        "Human", "Tree", "Wolf", "Sponge", "Paper", 
        "Air", "Water", "Dragon", "Devil", "Lightning", 
        "Gun", "Rock", "Fire", "Scissors", "Snake"
    ]

def determinar_ganador(jugador, computadora):
    # Diccionario basado en las reglas de Nivel 2 [cite: 1-16]
    reglas = {
        "Human": ["Tree", "Wolf", "Sponge", "Paper", "Air", "Water", "Dragon"], # [cite: 1, 2]
        "Tree": ["Wolf", "Sponge", "Paper", "Air", "Water", "Dragon", "Devil"], # [cite: 2, 3]
        "Wolf": ["Sponge", "Paper", "Air", "Water", "Dragon", "Devil", "Lightning"], # [cite: 3, 4]
        "Sponge": ["Paper", "Air", "Water", "Dragon", "Devil", "Lightning", "Gun"], # [cite: 4, 5]
        "Paper": ["Air", "Water", "Dragon", "Devil", "Lightning", "Gun", "Rock"], # [cite: 5, 6]
        "Air": ["Water", "Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire"], # [cite: 6, 7]
        "Water": ["Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors"], # [cite: 7, 8]
        "Dragon": ["Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake"], # [cite: 8, 9]
        "Devil": ["Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake", "Human"], # [cite: 9, 10]
        "Lightning": ["Gun", "Rock", "Fire", "Scissors", "Snake", "Human", "Tree"], # [cite: 10, 11]
        "Gun": ["Rock", "Fire", "Scissors", "Snake", "Human", "Tree", "Wolf"], # [cite: 11, 12]
        "Rock": ["Fire", "Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge"], # 
        "Fire": ["Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge", "Paper"], # [cite: 13, 14]
        "Scissors": ["Snake", "Human", "Tree", "Wolf", "Sponge", "Paper", "Air"], # [cite: 14, 15]
        "Snake": ["Human", "Tree", "Wolf", "Sponge", "Paper", "Air", "Water"] # [cite: 15, 16]
    }
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

def mostrar_menu(opciones):
    print("\n--- SELECCIONA TU MOVIMIENTO ---")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    print("---------------------------------")

def actualizar_marcador(resultado, v, d, e):
    """
    Actualiza los contadores globales basándose en el resultado de la ronda.
    """
    if resultado == "Victoria":
        v += 1
    elif resultado == "Derrota":
        d += 1
    else:
        e += 1
    return v, d, e

def mostrar_estadisticas(v, d, e):
    """
    Muestra el marcador actual de forma visual en la terminal.
    """
    print("\n" + "="*30)
    print(f"📊 MARCADOR ACTUAL:")
    print(f"🏆 Victorias: {v}")
    print(f"💀 Derrotas:  {d}")
    print(f"🤝 Empates:   {e}")
    print("="*30 + "\n")

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

def generar_eleccion_computadora(opciones):
    """
    Selecciona un elemento aleatorio de la lista de opciones.
    """
    eleccion_ia = random.choice(opciones)
    print(f"\n🤖 La computadora ha elegido: {eleccion_ia}")
    return eleccion_ia

# Ejemplo de uso:
# eleccion_final = capturar_eleccion_jugador()
opciones_disponibles = obtener_opciones()
jugador = capturar_eleccion_jugador()
computadora = generar_eleccion_computadora(opciones_disponibles)
resultado_ronda = determinar_ganador(jugador, computadora)
victorias, derrotas, empates = actualizar_marcador(resultado_ronda, victorias, derrotas, empates)
mostrar_estadisticas(victorias, derrotas, empates)