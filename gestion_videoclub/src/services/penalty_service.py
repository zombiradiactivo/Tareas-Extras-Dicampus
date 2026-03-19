from src.database.db_handler import get_connection
from src.models.rental import Alquiler

class PenaltyService:
    @staticmethod
    def registrar_multa_si_aplica(alquiler: Alquiler):
        """
        Si el alquiler tiene retraso, inserta un registro en la tabla de multas.
        """
        monto = alquiler.calcular_multa_actual()
        
        if monto > 0:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO multas (id_alquiler, monto, pagada)
                    VALUES (?, ?, 0)
                """, (alquiler.id, monto))
                conn.commit()
                print(f"⚠️ Multa de {monto:.2f}€ registrada para el alquiler ID: {alquiler.id}")
            except Exception as e:
                print(f"❌ Error al registrar multa: {e}")
            finally:
                conn.close()
        return monto