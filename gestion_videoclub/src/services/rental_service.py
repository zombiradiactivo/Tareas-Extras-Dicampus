from datetime import date, timedelta
from typing import Optional
from src.database.db_handler import get_connection
from src.models.rental import Alquiler
from src.services.penalty_service import PenaltyService

TARIFA_MULTA_DIARIA = 2.50
DIAS_PRESTAMO_ESTANDAR = 7

class RentalService:
    @staticmethod
    def registrar_alquiler(id_cliente: int, id_pelicula: int) -> bool:
        """
        Registra un alquiler: Valida stock, descuenta copia y guarda en DB.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. Verificar stock disponible
            cursor.execute("SELECT copias_disponibles FROM peliculas WHERE id = ?", (id_pelicula,))
            resultado = cursor.fetchone()
            
            if not resultado or resultado[0] <= 0:
                print("❌ Error: No hay copias disponibles de esta película.")
                return False

            # 2. Preparar fechas
            hoy = date.today()
            entrega_prevista = hoy + timedelta(days=DIAS_PRESTAMO_ESTANDAR)

            # 3. Insertar Alquiler
            cursor.execute("""
                INSERT INTO alquileres (id_cliente, id_pelicula, fecha_alquiler, fecha_prevista)
                VALUES (?, ?, ?, ?)
            """, (id_cliente, id_pelicula, hoy.isoformat(), entrega_prevista.isoformat()))

            # 4. Actualizar Stock (-1 copia)
            cursor.execute("""
                UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 
                WHERE id = ?
            """, (id_pelicula,))

            conn.commit()
            print(f"✅ Alquiler registrado. Devolver antes de: {entrega_prevista}")
            return True

        except Exception as e:
            conn.rollback()
            print(f"❌ Error en la transacción: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def procesar_devolucion(id_alquiler: int) -> float:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 1. Obtener datos crudos de la DB
            cursor.execute("""
                SELECT id_cliente, id_pelicula, fecha_alquiler, fecha_prevista 
                FROM alquileres 
                WHERE id = ? AND fecha_entrega_real IS NULL
            """, (id_alquiler,))
            
            row = cursor.fetchone()

            if not row:
                print("❌ Error: Alquiler no encontrado o ya devuelto.")
                return 0.0

            # 2. CONVERTIR A MODELO (Crucial para usar la lógica de multas)
            # Desempaquetamos la fila y creamos el objeto Alquiler
            id_cliente, id_pelicula, f_alquiler, f_prevista = row
            
            alquiler_obj = Alquiler(
                id_cliente=id_cliente,
                id_pelicula=id_pelicula,
                fecha_alquiler=date.fromisoformat(f_alquiler),
                fecha_prevista=date.fromisoformat(f_prevista),
                id=id_alquiler
            )

            # 3. Calcular multa usando el método del modelo
            multa_total = alquiler_obj.calcular_multa_actual()

            # 4. Actualizar registro de alquiler en DB
            hoy = date.today()
            cursor.execute("""
                UPDATE alquileres SET fecha_entrega_real = ? WHERE id = ?
            """, (hoy.isoformat(), id_alquiler))

            # 5. Reponer Stock (+1 copia)
            cursor.execute("""
                UPDATE peliculas SET copias_disponibles = copias_disponibles + 1 
                WHERE id = ?
            """, (id_pelicula,))

            # 6. Registrar la multa en su propia tabla si aplica
            if multa_total > 0:
                # Le pasamos el objeto ya actualizado con la fecha de hoy
                alquiler_obj.fecha_entrega_real = hoy
                PenaltyService.registrar_multa_si_aplica(alquiler_obj)
                print(f"⚠️ El cliente tiene una deuda de {multa_total:.2f}€ por retraso.")
            else:
                print("✅ Devolución exitosa sin cargos adicionales.")

            conn.commit()
            return multa_total

        except Exception as e:
            conn.rollback()
            print(f"❌ Error al devolver: {e}")
            return 0.0
        finally:
            conn.close()