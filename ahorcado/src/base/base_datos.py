import sqlite3
import os

def conectar():
    """Establece conexión con la base de datos en la carpeta /data."""
    # Asegura que la carpeta data exista
    if not os.path.exists('data'):
        os.makedirs('data')
    
    return sqlite3.connect('data/palabras.db')

def inicializar_db():
    """Crea la tabla e inserta las 20 palabras iniciales."""
    conn = conectar()
    cursor = conn.cursor()

    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS palabras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            dificultad TEXT NOT NULL
        )
    ''')

    # Datos iniciales ampliados (60 palabras en total)
    palabras_iniciales = [
        # PROGRAMACIÓN
        ('PYTHON', 'Programación', 'Fácil'),
        ('VARIABLE', 'Programación', 'Fácil'),
        ('BUCLE', 'Programación', 'Fácil'),
        ('FUNCION', 'Programación', 'Fácil'),
        ('OBJETO', 'Programación', 'Fácil'),
        ('HERENCIA', 'Programación', 'Media'),
        ('DICCIONARIO', 'Programación', 'Media'),
        ('ENCAPSULAMIENTO', 'Programación', 'Difícil'),
        ('POLIMORFISMO', 'Programación', 'Difícil'),
        ('EXPRESION REGULAR', 'Programación', 'Difícil'),

        # INFORMÁTICA
        ('ALGORITMO', 'Informática', 'Difícil'),
        ('RECURSIVIDAD', 'Informática', 'Difícil'),
        ('COMPILADOR', 'Informática', 'Difícil'),
        ('SISTEMA OPERATIVO', 'Informática', 'Media'),
        ('MEMORIA RAM', 'Informática', 'Fácil'),
        ('PROCESADOR', 'Informática', 'Fácil'),
        ('HARDWARE', 'Informática', 'Fácil'),
        ('SOFTWARE', 'Informática', 'Fácil'),
        ('INTELIGENCIA ARTIFICIAL', 'Informática', 'Media'),
        ('CIBERSEGURIDAD', 'Informática', 'Media'),

        # ASTRONOMÍA
        ('ESTRELLA', 'Astronomía', 'Fácil'),
        ('GALAXIA', 'Astronomía', 'Media'),
        ('TELESCOPIO', 'Astronomía', 'Media'),
        ('QUASAR', 'Astronomía', 'Difícil'),
        ('AGUJERO NEGRO', 'Astronomía', 'Difícil'),
        ('PLANETA', 'Astronomía', 'Fácil'),
        ('CONSTELACION', 'Astronomía', 'Media'),
        ('VIA LACTEA', 'Astronomía', 'Fácil'),
        ('SUPERNOVA', 'Astronomía', 'Difícil'),
        ('ASTRONAUTA', 'Astronomía', 'Fácil'),

        # MÚSICA
        ('GUITARRA', 'Música', 'Media'),
        ('ORQUESTA', 'Música', 'Difícil'),
        ('PIANO', 'Música', 'Fácil'),
        ('PARTITURA', 'Música', 'Media'),
        ('SINFONIA', 'Música', 'Difícil'),
        ('METRONOMO', 'Música', 'Difícil'),
        ('ACORDE', 'Música', 'Fácil'),
        ('PENTAGRAMA', 'Música', 'Media'),
        ('BATERIA', 'Música', 'Fácil'),
        ('SOLFEO', 'Música', 'Media'),

        # VIDEOJUEGOS (Nueva categoría)
        ('SUPER MARIO', 'Videojuegos', 'Fácil'),
        ('THE LEGEND OF ZELDA', 'Videojuegos', 'Media'),
        ('MINECRAFT', 'Videojuegos', 'Fácil'),
        ('GRAND THEFT AUTO', 'Videojuegos', 'Media'),
        ('RESIDENT EVIL', 'Videojuegos', 'Media'),
        ('ELDEN RING', 'Videojuegos', 'Difícil'),
        ('HOLLOW KNIGHT', 'Videojuegos', 'Difícil'),
        ('CONSOLA', 'Videojuegos', 'Fácil'),
        ('MULTIJUGADOR', 'Videojuegos', 'Media'),
        ('PANTALLA DE CARGA', 'Videojuegos', 'Media'),

        # REDES / BASE DE DATOS
        ('SERVIDOR', 'Redes / Bases de datos', 'Media'),
        ('CLIENTE', 'Redes / Bases de datos', 'Fácil'),
        ('SQLITE', 'Redes / Bases de datos', 'Media'),
        ('PROTOCOLO', 'Redes / Bases de datos', 'Media'),
        ('DIRECCION IP', 'Redes / Bases de datos', 'Fácil'),
        ('CORTAFUEGOS', 'Redes / Bases de datos', 'Difícil'),
        ('CONSULTA SQL', 'Redes / Bases de datos', 'Media'),
        ('LLAVE PRIMARIA', 'Redes / Bases de datos', 'Media'),
        ('MODELO RELACIONAL', 'Redes / Bases de datos', 'Difícil'),
        ('INDICE', 'Redes / Bases de datos', 'Fácil')
    ]

    try:
        cursor.executemany('''
            INSERT OR IGNORE INTO palabras (palabra, categoria, dificultad) 
            VALUES (?, ?, ?)
        ''', palabras_iniciales)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")
    finally:
        conn.close()

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

def insertar_palabra(palabra, categoria, dificultad):
    """Inserta una nueva palabra tras verificar que no existe."""
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # El UNIQUE en la tabla evitará duplicados a nivel DB
        cursor.execute('''
            INSERT INTO palabras (palabra, categoria, dificultad)
            VALUES (?, ?, ?)
        ''', (palabra, categoria, dificultad))
        
        conn.commit()
        return True, "Palabra añadida correctamente."

    except sqlite3.IntegrityError:
        return False, "⚠️ Esa palabra ya existe en la base de datos."
    except sqlite3.Error as e:
        return False, f"❌ Error crítico de base de datos: {e}"
    finally:
        if conn:
            conn.close()
# Test

if __name__ == "__main__":
    inicializar_db()
    obtener_todas_las_palabras()