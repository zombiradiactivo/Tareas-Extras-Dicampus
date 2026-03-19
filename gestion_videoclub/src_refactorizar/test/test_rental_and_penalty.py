from datetime import date, timedelta
from src_refactorizar.database import db_handler
from src_refactorizar.models.rental import Alquiler
from src_refactorizar.services.rental_service import RentalService
from src_refactorizar.services.penalty_service import PenaltyService
from src_refactorizar.services.catalog_service import CatalogService


def seed_base():
    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO peliculas (titulo, director, copias_disponibles) VALUES (?, ?, ?)",
                       ("Pelicula A", "Dir A", 1))
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                       ("Cliente A", "clienteA@mail.com"))
        conn.commit()


def test_registrar_alquiler_sin_stock():
    seed_base()
    rs = RentalService()
    # id_pelicula 1 tiene solo 1 copia y se reducirá a 0 cuando se alquile una vez
    assert rs.registrar_alquiler(1, 1) is True
    # intentar alquilar de nuevo con stock 0 debe fallar
    assert rs.registrar_alquiler(1, 1) is False


def test_procesar_devolucion_no_existente():
    rs = RentalService()
    assert rs.procesar_devolucion(999) == 0.0


def test_procesar_devolucion_con_multas_y_actualizacion_stock():
    seed_base()
    rs = RentalService()

    assert rs.registrar_alquiler(1, 1) is True

    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT copias_disponibles FROM peliculas WHERE id = ?", (1,))
        stock = cursor.fetchone()[0]
    assert stock == 0

    # Simular que la fecha prevista ya pasó para que existan multas
    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE alquileres SET fecha_prevista = ? WHERE id = ?", ((date.today() - timedelta(days=10)).isoformat(), 1))
        conn.commit()

    multa = rs.procesar_devolucion(1)
    assert multa > 0

    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT copias_disponibles FROM peliculas WHERE id = ?", (1,))
        stock_final = cursor.fetchone()[0]
    assert stock_final == 1

    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT monto FROM multas WHERE id_alquiler = ?", (1,))
        row = cursor.fetchone()
    assert row is not None and row[0] == multa


def test_penalty_service_calcula_y_registra_multa():
    # Alquiler con 3 días de retraso (2.0€ por día) -> 6.0€
    alquiler = Alquiler(
        id_cliente=1,
        id_pelicula=1,
        fecha_alquiler=date.today() - timedelta(days=10),
        fecha_prevista=date.today() - timedelta(days=3),
        fecha_entrega_real=date.today(),
        id=42,
    )
    monto = PenaltyService.registrar_multa_si_aplica(alquiler)
    assert monto == 6.0

    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT monto FROM multas WHERE id_alquiler = ?", (42,))
        row = cursor.fetchone()
    assert row is not None and row[0] == 6.0


def test_devolver_sin_retraso():
    seed_base()
    rs = RentalService()
    assert rs.registrar_alquiler(1, 1) is True

    # Devolver a tiempo con fecha_prevista actual
    multa = rs.procesar_devolucion(1)
    assert multa == 0.0

    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT copias_disponibles FROM peliculas WHERE id = ?", (1,))
        stock_final = cursor.fetchone()[0]
    assert stock_final == 1


def test_calcular_multa_dias_negativos():
    alquiler = Alquiler(
        id_cliente=1,
        id_pelicula=1,
        fecha_alquiler=date.today(),
        fecha_prevista=date.today() + timedelta(days=7),
        fecha_entrega_real=date.today(),
        id=99,
    )
    assert alquiler.calcular_multa_actual() == 0.0

