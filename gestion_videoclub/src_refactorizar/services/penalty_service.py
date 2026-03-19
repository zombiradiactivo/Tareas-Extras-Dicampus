from src_refactorizar.database.db_handler import db_connection
from src_refactorizar.models.rental import Alquiler


class PenaltyService:
    @staticmethod
    def registrar_multa_si_aplica(alquiler: Alquiler):
        """Si el alquiler tiene retraso, inserta un registro en la tabla de multas."""
        monto = alquiler.calcular_multa_actual()

        if monto <= 0:
            return monto

        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO multas (id_alquiler, monto, pagada) VALUES (?, ?, 0)",
                (alquiler.id, monto),
            )
            conn.commit()

        print(f"⚠️ Multa de {monto:.2f}€ registrada para el alquiler ID: {alquiler.id}")
        return monto