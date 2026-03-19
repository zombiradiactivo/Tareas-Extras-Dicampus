import random

def calcular_estadisticas(historial_tiradas):
    """
    Calcula y muestra estadísticas detalladas: suma, media, máximo y mínimo.
    """
    # Extraemos la suma de cada tirada para facilitar los cálculos
    sumas_parciales = [sum(tirada) for tirada in historial_tiradas]
    
    total_global = sum(sumas_parciales)
    media = total_global / len(sumas_parciales)
    
    # Encontrar valores y sus índices (sumas_parciales.index devuelve el primero encontrado)
    max_valor = max(sumas_parciales)
    min_valor = min(sumas_parciales)
    
    indice_max = sumas_parciales.index(max_valor) + 1
    indice_min = sumas_parciales.index(min_valor) + 1

    print("\n" + "="*30)
    print("📊 ESTADÍSTICAS DE LA SESIÓN")
    print("="*30)
    print(f"🔹 Suma Total:      {total_global}")
    print(f"🔹 Media x Tirada:  {media:.2f}")
    print(f"🔹 Valor Máximo:    {max_valor} (Tirada #{indice_max})")
    print(f"🔹 Valor Mínimo:    {min_valor} (Tirada #{indice_min})")
    print("="*30)

def lanzar_dados(caras, cantidad, repeticiones):
    """
    Simula las tiradas y almacena los resultados para su análisis.
    """
    historial_sesion = []

    print(f"\n--- Generando {repeticiones} series de {cantidad}d{caras} ---")

    for i in range(1, repeticiones + 1):
        tirada_actual = [random.randint(1, caras) for _ in range(cantidad)]
        suma_parcial = sum(tirada_actual)
        historial_sesion.append(tirada_actual)
        
        print(f"Tirada #{i}: {tirada_actual} | Suma: {suma_parcial}")

    # Llamada a la nueva función de estadísticas
    calcular_estadisticas(historial_sesion)
    return historial_sesion

def obtener_entero_validado(mensaje, min_val, max_val):
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            valor = int(entrada)
            if min_val <= valor <= max_val:
                return valor
        print(f"❌ Error: Introduce un número entre {min_val} y {max_val}.")

def seleccionar_dado():
    dados_validos = {"4": 4, "6": 6, "8": 8, "10": 10, "12": 12, "20": 20}
    while True:
        print("\n--- Menú de Dados ---")
        print("Disponibles: D4, D6, D8, D10, D12, D20")
        eleccion = input("Elige el número de caras (o escribe 'salir'): ").strip()
        if eleccion.lower() == 'salir': return None
        if eleccion in dados_validos: return dados_validos[eleccion]
        print("❌ Error: Tipo de dado no válido.")

if __name__ == "__main__":
    caras = seleccionar_dado()
    if caras:
        cantidad = obtener_entero_validado("¿Cuántos dados? (1-10): ", 1, 10)
        repeticiones = obtener_entero_validado("¿Cuántas repeticiones? (1-20): ", 1, 20)
        lanzar_dados(caras, cantidad, repeticiones)