from src_refactorizar.database.db_handler import db_connection


class CustomerService:
    @staticmethod
    def listar_clientes():
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, email FROM clientes")
            rows = cursor.fetchall()

        return [
            {
                "id": r[0],
                "nombre": r[1],
                "email": r[2],
            }
            for r in rows
        ]

    @staticmethod
    def obtener_cliente_por_id(id_cliente: int):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, email FROM clientes WHERE id = ?",
                (id_cliente,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
        }