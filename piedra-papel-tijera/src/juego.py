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

def jugar_partida():
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
        print(f"\n🔔 RONDA {ronda_actual} de {total_rondas}")
        
        # Turno del Jugador
        jugador = capturar_eleccion_jugador()
        
        # Turno de la Computadora
        computadora = generar_eleccion_computadora(opciones)
        
        # Combate y Resultado
        resultado = determinar_ganador(jugador, computadora)
        
        # Actualización de Estadísticas
        v, d, e = actualizar_marcador(resultado, v, d, e)
        mostrar_estadisticas(v, d, e)

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