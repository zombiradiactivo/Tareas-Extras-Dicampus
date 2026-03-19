import random

def lanzar_dado(caras):
    """
    Simula el lanzamiento de un dado con el número de caras especificado.
    """
    resultado = random.randint(1, caras)
    print(f"\n🎲 Resultado del lanzamiento (D{caras}): {resultado}")

def seleccionar_dado():
    """
    Muestra el menú y valida la selección del usuario.
    """
    dados_validos = {
        "4": 4,
        "6": 6,
        "8": 8,
        "10": 10,
        "12": 12,
        "20": 20
    }

    while True:
        print("\n--- Menú de Dados ---")
        print("Disponibles: D4, D6, D8, D10, D12, D20")
        eleccion = input("Elige el número de caras (o escribe 'salir'): ").strip()

        if eleccion.lower() == 'salir':
            return None

        if eleccion in dados_validos:
            return dados_validos[eleccion]
        else:
            print("❌ Error: Tipo de dado no válido. Inténtalo de nuevo.")

if __name__ == "__main__":
    caras_seleccionadas = seleccionar_dado()
    if caras_seleccionadas:
        lanzar_dado(caras_seleccionadas)