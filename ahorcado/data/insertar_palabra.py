from data.db import conectar
import sqlite3

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
