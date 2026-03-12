import os
import random

# 1. Inicialización de variables (Marcador)
victorias = 0
derrotas = 0
empates = 0


def limpiar_pantalla():
    # Limpia la terminal según el sistema operativo (Windows o Unix/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_emoji(opcion):
    # Mapeo de emojis para las 15 variantes [cite: 1-16]
    emojis = {
        "Human": "👤", "Tree": "🌳", "Wolf": "🐺", "Sponge": "🧽", "Paper": "📄",
        "Air": "💨", "Water": "💧", "Dragon": "🐉", "Devil": "😈", "Lightning": "⚡",
        "Gun": "🔫", "Rock": "🪨", "Fire": "🔥", "Scissors": "✂️", "Snake": "🐍"
    }
    return emojis.get(opcion, "❓")

def mostrar_bienvenida():
    limpiar_pantalla()
    print("="*50)
    print("      SÚPER PIEDRA-PAPEL-TIJERAS: NIVEL 2      ")
    print("="*50)
    input("\nPresiona ENTER para configurar tu partida...")

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
        "Human": ["Tree", "Wolf", "Sponge", "Paper", "Air", "Water", "Dragon"],
        "Tree": ["Wolf", "Sponge", "Paper", "Air", "Water", "Dragon", "Devil"],
        "Wolf": ["Sponge", "Paper", "Air", "Water", "Dragon", "Devil", "Lightning"], 
        "Sponge": ["Paper", "Air", "Water", "Dragon", "Devil", "Lightning", "Gun"], 
        "Paper": ["Air", "Water", "Dragon", "Devil", "Lightning", "Gun", "Rock"],
        "Air": ["Water", "Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire"], 
        "Water": ["Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors"], 
        "Dragon": ["Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake"], 
        "Devil": ["Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake", "Human"], 
        "Lightning": ["Gun", "Rock", "Fire", "Scissors", "Snake", "Human", "Tree"], 
        "Gun": ["Rock", "Fire", "Scissors", "Snake", "Human", "Tree", "Wolf"], 
        "Rock": ["Fire", "Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge"], 
        "Fire": ["Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge", "Paper"], 
        "Scissors": ["Snake", "Human", "Tree", "Wolf", "Sponge", "Paper", "Air"], 
        "Snake": ["Human", "Tree", "Wolf", "Sponge", "Paper", "Air", "Water"] 
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
    print(f"Porcentaje Victorias:   {(v/(v + d + e))*100:.0f}%")

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

def jugar_partida():
    mostrar_bienvenida()
    # 1. Configuración de la partida
    while True:
        try:
            total_rondas = int(input("¿Cuántas rondas quieres jugar?: "))
            if total_rondas > 0:
                break
            print("❌ Por favor, introduce un número mayor que 0.")
        except ValueError:
            print("❌ Entrada no válida. Debes introducir un número entero.")

    # Inicialización de marcadores y opciones
    v, d, e = 0, 0, 0
    opciones = obtener_opciones()
    
    # 2. Bucle principal del juego
    for ronda_actual in range(1, total_rondas + 1):
        limpiar_pantalla()
        print(f"✨ RONDA {ronda_actual} de {total_rondas} ✨")
        print(f"Marcador actual: 🏆 {v} | 💀 {d} | 🤝 {e}")
        print("-" * 30)        
        # Turno del Jugador
        limpiar_pantalla()
        jugador = capturar_eleccion_jugador()
        emoji_jugador = obtener_emoji(jugador)
        
        # Turno de la Computadora
        computadora = generar_eleccion_computadora(opciones)
        emoji_ia = obtener_emoji(computadora)

        print(f"\nSimbología del duelo:")
        print(f"Tú: {emoji_jugador} {jugador}  VS  IA: {emoji_ia} {computadora}")
        print("-" * 30)

        # Combate y Resultado
        resultado = determinar_ganador(jugador, computadora)
        
        # Actualización de Estadísticas
        v, d, e = actualizar_marcador(resultado, v, d, e)
        mostrar_estadisticas(v, d, e)
        if ronda_actual != total_rondas:
            input("\nPresiona ENTER para continuar tu partida...")


    # 3. Cierre de la partida
    print("\n--- ¡PARTIDA FINALIZADA! ---")
    if v > d:
        print("🎉 ¡Felicidades! Has ganado la sesión.")
    elif d > v:
        print("💀 La computadora ha ganado esta vez. ¡Sigue intentándolo!")
    else:
        print("🤝 ¡Ha sido un empate técnico!")

if __name__ == "__main__":
    jugar_partida()