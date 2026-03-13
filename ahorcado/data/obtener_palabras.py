from data.db import conectar

def obtener_todas_las_palabras():
    """Consulta y muestra todas las palabras almacenadas."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM palabras")
    filas = cursor.fetchall()
    
    print("\n--- Diccionario de Palabras ---")
    print(f"{'ID':<5} {'Palabra':<15} {'Categoría':<15} {'Dificultad':<10}")
    print("-" * 50)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<15} {f[2]:<15} {f[3]:<10}")
    
    conn.close()
    return filas

def obtener_palabra_filtrada(categoria_seleccionada=None):
    """Obtiene una palabra aleatoria filtrada por categoría."""
    conn = conectar()
    cursor = conn.cursor()
    
    if categoria_seleccionada:
        query = "SELECT palabra, categoria, dificultad FROM palabras WHERE categoria = ? ORDER BY RANDOM() LIMIT 1"
        cursor.execute(query, (categoria_seleccionada,))
    else:
        query = "SELECT palabra, categoria, dificultad FROM palabras ORDER BY RANDOM() LIMIT 1"
        cursor.execute(query)
        
    resultado = cursor.fetchone()
    conn.close()
    return resultado
