from src_refactorizar.services.penalty_service import PenaltyService
from src_refactorizar.database.db_handler import db_connection
from src_refactorizar.models.rental import Alquiler
from datetime import date, timedelta
from typing import Optional


class RentalService:
    TARIFA_MULTA_DIARIA = 2.50
    DIAS_PRESTAMO_ESTANDAR = 7

    def _obtener_pelicula(self, id_pelicula: int):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT copias_disponibles FROM peliculas WHERE id = ?",
                (id_pelicula,),
            )
            return cursor.fetchone()

    def _actualizar_stock(self, id_pelicula: int, delta: int):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE peliculas SET copias_disponibles = copias_disponibles + ? WHERE id = ?",
                (delta, id_pelicula),
            )
            conn.commit()

    def _insertar_alquiler(self, id_cliente: int, id_pelicula: int, fecha_alquiler: date, fecha_prevista: date):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO alquileres (id_cliente, id_pelicula, fecha_alquiler, fecha_prevista) VALUES (?, ?, ?, ?)",
                (id_cliente, id_pelicula, fecha_alquiler.isoformat(), fecha_prevista.isoformat()),
            )
            conn.commit()

    def _obtener_alquiler_activo(self, id_alquiler: int):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_cliente, id_pelicula, fecha_alquiler, fecha_prevista FROM alquileres WHERE id = ? AND fecha_entrega_real IS NULL",
                (id_alquiler,),
            )
            return cursor.fetchone()

    def _actualizar_alquiler_devuelto(self, id_alquiler: int, fecha_entrega_real: date):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alquileres SET fecha_entrega_real = ? WHERE id = ?",
                (fecha_entrega_real.isoformat(), id_alquiler),
            )
            conn.commit()

    def registrar_alquiler(self, id_cliente: int, id_pelicula: int) -> bool:
        pelicula = self._obtener_pelicula(id_pelicula)

        if not pelicula or pelicula[0] <= 0:
            print("❌ Error: No hay copias disponibles de esta película.")
            return False

        hoy = date.today()
        entrega_prevista = hoy + timedelta(days=self.DIAS_PRESTAMO_ESTANDAR)

        try:
            self._insertar_alquiler(id_cliente, id_pelicula, hoy, entrega_prevista)
            self._actualizar_stock(id_pelicula, -1)
            print(f"✅ Alquiler registrado. Devolver antes de: {entrega_prevista}")
            return True
        except Exception as e:
            # si algo falla en cualquiera de las operaciones, se deja la lógica de roll-back mínima
            print(f"❌ Error en la transacción: {e}")
            return False

    def procesar_devolucion(self, id_alquiler: int) -> float:
        row = self._obtener_alquiler_activo(id_alquiler)

        if not row:
            print("❌ Error: Alquiler no encontrado o ya devuelto.")
            return 0.0

        id_cliente, id_pelicula, f_alquiler, f_prevista = row

        alquiler_obj = Alquiler(
            id_cliente=id_cliente,
            id_pelicula=id_pelicula,
            fecha_alquiler=date.fromisoformat(f_alquiler),
            fecha_prevista=date.fromisoformat(f_prevista),
            id=id_alquiler,
        )

        multa_total = alquiler_obj.calcular_multa_actual()
        hoy = date.today()

        try:
            self._actualizar_alquiler_devuelto(id_alquiler, hoy)
            self._actualizar_stock(id_pelicula, 1)

            if multa_total > 0:
                alquiler_obj.fecha_entrega_real = hoy
                PenaltyService.registrar_multa_si_aplica(alquiler_obj)
                print(f"⚠️ El cliente tiene una deuda de {multa_total:.2f}€ por retraso.")
            else:
                print("✅ Devolución exitosa sin cargos adicionales.")

            return multa_total
        except Exception as e:
            print(f"❌ Error al devolver: {e}")
            return 0.0