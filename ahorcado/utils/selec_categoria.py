from data.obtener_estadisticas import obtener_estadisticas_categorias

def seleccionar_categoria():
    """Muestra categorías y permite al usuario elegir una."""
    stats = obtener_estadisticas_categorias()
    
    print("\n--- CATEGORÍAS DISPONIBLES ---")
    print(f"{'#':<3} {'Categoría':<20} {'Palabras':<10}")
    print("-" * 35)
    
    categorias_lista = []
    for i, (nombre, total) in enumerate(stats, 1):
        print(f"{i:<3} {nombre:<20} {total:<10}")
        categorias_lista.append(nombre)
    
    print(f"{len(categorias_lista) + 1}: Todas (Aleatorio)")

    try:
        seleccion = int(input("\nSelecciona el número de categoría: "))
        if 1 <= seleccion <= len(categorias_lista):
            return categorias_lista[seleccion - 1]
        else:
            return None # Opción "Todas"
    except ValueError:
        print("Entrada no válida. Se elegirá una categoría al azar.")
        return None
