
def calcular_estadisticas(historial_tiradas):
    """
    Calcula métricas descriptivas de una serie de lanzamientos.

    Procesa las sumas de cada tirada para obtener el total global,
    el promedio aritmético y los valores extremos.

    Args:
        historial_tiradas (list): Los datos brutos de la serie.

    Returns:
        dict: Un diccionario con las claves 'Total', 'Media', 'Máximo' y 'Mínimo'.
    """
    sumas = [sum(t) for t in historial_tiradas]
    stats = {
        "Total": sum(sumas),
        "Media": round(sum(sumas) / len(sumas), 2),
        "Máximo": max(sumas),
        "Mínimo": min(sumas)
    }
    print("\n📈 ESTADÍSTICAS ACUMULADAS:")
    for k, v in stats.items():
        print(f" - {k}: {v}")
    return stats