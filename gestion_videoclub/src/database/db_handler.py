import sqlite3

def get_connection():
    return sqlite3.connect("video_club.db")

def create_tables():
    conn = get_connection()
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
    
    conn.commit()
    conn.close()