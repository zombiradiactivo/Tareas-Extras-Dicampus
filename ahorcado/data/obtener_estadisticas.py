from data.db import conectar

def obtener_estadisticas_categorias():
    """Retorna una lista de categorías y el conteo de palabras en cada una."""
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
        SELECT categoria, COUNT(*) as total 
        FROM palabras 
        GROUP BY categoria 
        ORDER BY categoria ASC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados
