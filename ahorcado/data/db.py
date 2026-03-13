import sqlite3
import os
from config.config import PALABRAS_INICIALES as palabras_iniciales

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
