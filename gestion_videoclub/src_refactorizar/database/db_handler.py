import sqlite3
from contextlib import contextmanager

DB_PATH = "video_club.db"

@contextmanager
def db_connection():
    """Context manager para conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_connection():
    """Compatibilidad con API anterior."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    with db_connection() as conn:
        cursor = conn.cursor()

        # Tabla Películas
        cursor.execute('''CREATE TABLE IF NOT EXISTS peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            director TEXT,
            copias_disponibles INTEGER DEFAULT 1
        )''')

        # Tabla Clientes
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE
        )''')

        # Tabla Alquileres
        cursor.execute('''CREATE TABLE IF NOT EXISTS alquileres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            id_pelicula INTEGER,
            fecha_alquiler DATE,
            fecha_prevista DATE,
            fecha_entrega_real DATE,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id),
            FOREIGN KEY(id_pelicula) REFERENCES peliculas(id)
        )''')

        # Tabla Multas
        cursor.execute('''CREATE TABLE IF NOT EXISTS multas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alquiler INTEGER,
            monto REAL NOT NULL,
            pagada INTEGER DEFAULT 0,
            FOREIGN KEY(id_alquiler) REFERENCES alquileres(id)
        )''')

        conn.commit()