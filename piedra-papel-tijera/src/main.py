from utils.utils import determinar_ganador, generar_eleccion_computadora, limpiar_pantalla, obtener_opciones
from utils.variables import actualizar_marcador, mostrar_estadisticas
from utils.IO import capturar_eleccion_jugador, obtener_emoji
from utils.cli_menus import mostrar_bienvenida


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