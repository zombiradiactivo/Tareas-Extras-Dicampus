def mostrar_histograma(historial_tiradas, caras):
    """
    Genera una representación visual de la frecuencia de resultados.

    Calcula cuántas veces apareció cada cara y muestra una barra
    proporcional usando el carácter '■'.

    Args:
        historial_tiradas (list): Lista con todos los lanzamientos.
        caras (int): Rango máximo del dado para el eje del histograma.
    """
    todos_los_numeros = [v for t in historial_tiradas for v in t]
    frecuencias = {c: todos_los_numeros.count(c) for c in range(1, caras + 1)}
    max_f = max(frecuencias.values()) if frecuencias.values() else 0
    
    print("\n📊 HISTOGRAMA DE FRECUENCIAS:")
    for cara, cuenta in frecuencias.items():
        barra = "■" * (int((cuenta / max_f) * 20) if max_f > 0 else 0)
        print(f"Cara {cara:2}: {barra} ({cuenta})")
