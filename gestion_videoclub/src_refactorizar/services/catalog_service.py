from src_refactorizar.database.db_handler import db_connection

class CatalogService:
    @staticmethod
    def listar_peliculas():
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, titulo, director, copias_disponibles FROM peliculas")
            rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "titulo": r[1],
                "director": r[2],
                "copias_disponibles": r[3],
            }
            for r in rows
        ]

    @staticmethod
    def obtener_pelicula_por_id(id_pelicula: int):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, titulo, director, copias_disponibles FROM peliculas WHERE id = ?",
                (id_pelicula,),
            )
            row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "titulo": row[1],
            "director": row[2],
            "copias_disponibles": row[3],
        }