import random

def lanzar_dados(caras, cantidad, repeticiones):
    """
    Simula series de lanzamientos y muestra resultados detallados y globales.
    """
    historial_sesion = []
    suma_global = 0

    print(f"\n--- Iniciando {repeticiones} tiradas de {cantidad}d{caras} ---")

    for i in range(1, repeticiones + 1):
        tirada_actual = [random.randint(1, caras) for _ in range(cantidad)]
        suma_parcial = sum(tirada_actual)
        suma_global += suma_parcial
        historial_sesion.append(tirada_actual)
        
        print(f"Tirada #{i}: {tirada_actual} | Suma Parcial: {suma_parcial}")

    print("-" * 40)
    print(f"📊 SUMA GLOBAL DE TODAS LAS TIRADAS: {suma_global}")
    return historial_sesion

def obtener_entero_validado(mensaje, min_val, max_val):
    """
    Función genérica para validar entradas numéricas en un rango.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            valor = int(entrada)
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"❌ Error: El número debe estar entre {min_val} y {max_val}.")
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
        print("❌ Error: Tipo de dado no válido.")

if __name__ == "__main__":
    caras = seleccionar_dado()
    if caras:
        cantidad = obtener_entero_validado("¿Cuántos dados quieres lanzar? (1-10): ", 1, 10)
        repeticiones = obtener_entero_validado("¿Cuántas veces quieres repetir la tirada? (1-20): ", 1, 20)
        
        lanzar_dados(caras, cantidad, repeticiones)