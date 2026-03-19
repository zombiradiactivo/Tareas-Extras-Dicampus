import random

def lanzar_dados(caras, cantidad):
    """
    Simula el lanzamiento de múltiples dados y muestra resultados individuales y la suma.
    """
    resultados = []
    for _ in range(cantidad):
        resultados.append(random.randint(1, caras))
    
    suma_total = sum(resultados)
    
    print(f"\n🎲 Resultados (D{caras} x{cantidad}): {resultados}")
    print(f"📊 Suma total: {suma_total}")

def obtener_cantidad_dados():
    """
    Valida que el usuario elija un número de dados entre 1 y 10.
    """
    while True:
        entrada = input("¿Cuántos dados quieres lanzar? (1-10): ").strip()
        
        if entrada.isdigit():
            cantidad = int(entrada)
            if 1 <= cantidad <= 10:
                return cantidad
            else:
                print("❌ Error: Debes elegir entre 1 y 10 dados.")
        else:
            print("❌ Error: Por favor, introduce un número entero válido.")

def seleccionar_dado():
    """
    Muestra el menú y valida la selección del tipo de dado.
    """
    dados_validos = {"4": 4, "6": 6, "8": 8, "10": 10, "12": 12, "20": 20}

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
        cantidad_seleccionada = obtener_cantidad_dados()
        lanzar_dados(caras_seleccionadas, cantidad_seleccionada)