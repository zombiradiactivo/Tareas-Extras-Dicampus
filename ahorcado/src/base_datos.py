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

    # Datos iniciales (20 palabras)
    palabras_iniciales = [
        ('PYTHON', 'Programación', 'Fácil'),
        ('SQLITE', 'Base de Datos', 'Media'),
        ('ALGORITMO', 'Informática', 'Difícil'),
        ('VARIABLE', 'Programación', 'Fácil'),
        ('RECURSIVIDAD', 'Informática', 'Difícil'),
        ('INTERFAZ', 'Diseño', 'Media'),
        ('SERVIDOR', 'Redes', 'Media'),
        ('CLIENTE', 'Redes', 'Fácil'),
        ('COMPILADOR', 'Informática', 'Difícil'),
        ('BUCLE', 'Programación', 'Fácil'),
        ('FUNCION', 'Programación', 'Fácil'),
        ('OBJETO', 'Programación', 'Fácil'),
        ('HERENCIA', 'Programación', 'Media'),
        ('ESCRITORIO', 'Muebles', 'Fácil'),
        ('GUITARRA', 'Música', 'Media'),
        ('ORQUESTA', 'Música', 'Difícil'),
        ('ESTRELLA', 'Astronomía', 'Fácil'),
        ('GALAXIA', 'Astronomía', 'Media'),
        ('TELESCOPIO', 'Astronomía', 'Media'),
        ('QUASAR', 'Astronomía', 'Difícil')
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


# Test

if __name__ == "__main__":
    inicializar_db()
    obtener_todas_las_palabras()