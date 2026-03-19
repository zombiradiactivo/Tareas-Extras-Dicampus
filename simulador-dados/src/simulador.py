import random

def mostrar_histograma(historial_tiradas, caras):
    """
    Muestra un histograma de frecuencias de los valores obtenidos.
    """
    # Aplanamos la lista de listas para tener todos los números individuales
    todos_los_numeros = [valor for tirada in historial_tiradas for valor in tirada]
    
    # Contamos frecuencias para cada cara posible del dado
    frecuencias = {cara: todos_los_numeros.count(cara) for cara in range(1, caras + 1)}
    
    max_frecuencia = max(frecuencias.values()) if frecuencias.values() else 0
    ancho_maximo = 20  # Longitud máxima de la barra en caracteres

    print("\n📊 DISTRIBUCIÓN DE RESULTADOS (HISTOGRAMA)")
    print("-" * 40)
    
    for cara, cuenta in frecuencias.items():
        # Escalamiento: (cuenta / max_frecuencia) * ancho_maximo
        # Evitamos división por cero si no hay tiradas
        if max_frecuencia > 0:
            longitud_barra = int((cuenta / max_frecuencia) * ancho_maximo)
        else:
            longitud_barra = 0
            
        barra = "■" * longitud_barra
        print(f"Cara {cara:2}: {barra} ({cuenta})")
    print("-" * 40)

def calcular_estadisticas(historial_tiradas):
    sumas_parciales = [sum(tirada) for tirada in historial_tiradas]
    total_global = sum(sumas_parciales)
    media = total_global / len(sumas_parciales)
    max_valor = max(sumas_parciales)
    min_valor = min(sumas_parciales)
    
    print("\n" + "="*30)
    print("📈 RESUMEN DE LA SERIE")
    print(f"🔹 Suma Total:      {total_global}")
    print(f"🔹 Media x Tirada:  {media:.2f}")
    print(f"🔹 Valor Máximo:    {max_valor}")
    print(f"🔹 Valor Mínimo:    {min_valor}")
    print("="*30)

def lanzar_dados(caras, cantidad, repeticiones):
    historial_sesion = []
    for i in range(1, repeticiones + 1):
        tirada_actual = [random.randint(1, caras) for _ in range(cantidad)]
        historial_sesion.append(tirada_actual)
        print(f"Tirada #{i}: {tirada_actual} | Suma: {sum(tirada_actual)}")

    # Ejecutar visualizaciones
    calcular_estadisticas(historial_sesion)
    mostrar_histograma(historial_sesion, caras)
    return historial_sesion

def obtener_entero_validado(mensaje, min_val, max_val):
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit():
            valor = int(entrada)
            if min_val <= valor <= max_val: return valor
        print(f"❌ Error: Introduce un número entre {min_val} y {max_val}.")

def seleccionar_dado():
    dados_validos = {"4": 4, "6": 6, "8": 8, "10": 10, "12": 12, "20": 20}
    while True:
        print("\n--- Menú de Dados ---")
        eleccion = input("Elige el número de caras (4, 6, 8, 10, 12, 20) o 'salir': ").strip()
        if eleccion.lower() == 'salir': return None
        if eleccion in dados_validos: return dados_validos[eleccion]
        print("❌ Error: Tipo de dado no válido.")

if __name__ == "__main__":
    caras = seleccionar_dado()
    if caras:
        cantidad = obtener_entero_validado("¿Cuántos dados? (1-10): ", 1, 10)
        repeticiones = obtener_entero_validado("¿Cuántas repeticiones? (1-20): ", 1, 20)
        lanzar_dados(caras, cantidad, repeticiones)