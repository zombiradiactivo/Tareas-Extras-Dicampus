from pathlib import Path
import datetime
import pytest
import gc # Garbage Collector para forzar la liberación en Windows
import os

from refactorizaciones.v1.restaurant_reservations import ReservationSystem as V1System
from refactorizaciones.v2.repository import ReservationRepository as V2Repository
from refactorizaciones.v2.service import ReservationService as V2Service
from refactorizaciones.v3.repository import ReservationRepository as V3Repository
from refactorizaciones.v3.service import ReservationService as V3Service



@pytest.fixture(autouse=True)
def cleanup_benchmarks():
    # 1. Antes del test: Limpiar
    db_files = ["db/bench_v1.db", "db/bench_v2.db", "db/bench_v3.db"]
    for f in db_files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except PermissionError:
                pass # Si no se puede borrar ahora, se intentará luego

    yield 

    # 2. Después del test: Limpiar
    # IMPORTANTE: Eliminamos referencias y forzamos limpieza de memoria
    gc.collect() 

    for f in db_files:
        # Intentamos borrar también los archivos temporales de SQLite (-journal o -wal)
        for extra in ["", "-journal", "-wal", "-shm"]:
            path = f + extra
            if os.path.exists(path):
                try:
                    os.remove(path)
                except PermissionError:
                    # En Windows, a veces el SO tarda unos ms en soltar el archivo
                    print(f"No se pudo borrar {path}, todavía en uso.")


def _populate_service(service, num_customers=10, num_tables=5, reservations_per_table=100):
    customers = []
    for i in range(num_customers):
        c = service.add_customer(f"customer{i}", f"phone{i}", f"customer{i}@example.com")
        customers.append(c)

    tables = []
    for i in range(num_tables):
        t = service.add_table(number=i + 1, capacity=10, zone="interior")
        tables.append(t)

    now = datetime.datetime.now() + datetime.timedelta(days=1)

    for t in tables:
        for j in range(reservations_per_table):
            customer = customers[j % num_customers]
            start = now + datetime.timedelta(hours=j * 3)
            service.create_reservation(customer.customer_id, t.table_id, start, party_size=2)


def setup_benchmark_service(service_class, repo_class, db_filename):
    # Pasamos solo el nombre del archivo, no la ruta absoluta de tmp_path
    repo = repo_class(db_filename)
    service = service_class(repo)
    _populate_service(service, num_customers=10, num_tables=5, reservations_per_table=80)
    return service


def setup_v1_service(db_filename):
    # La V1 no tiene Repository separado, es un sistema completo
    system = V1System()
    # Importante: En V1, save_to_db crea las tablas y establece la ruta
    system.save_to_db(f"db/{db_filename}") 
    _populate_service(system, num_customers=10, num_tables=5, reservations_per_table=80)
    return system

@pytest.mark.benchmark(group="availability-check")
def test_benchmark_v1_availability(benchmark):
    # 1. SETUP
    service = setup_v1_service("bench_v1.db")
    table_id = list(service.tables.keys())[0]
    ref_time = datetime.datetime.now() + datetime.timedelta(days=1)

    # 2. EJECUCIÓN
    result = benchmark.pedantic(lambda: service.check_availability(table_id, ref_time, duration_hours=2.0),iterations=100, rounds=50)


    # Limpieza manual de conexión si fuera necesario (V1 usa sqlite3.connect en cada método)
    assert result is not None

@pytest.mark.benchmark(group="availability-check")
def test_benchmark_v2_availability(benchmark):
    # Usamos un nombre de archivo simple para evitar el ReservationError
    service = setup_benchmark_service(V2Service, V2Repository, "bench_v2.db")
    
    table_id = list(service.tables.keys())[0]
    ref_time = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # Ahora sí, el benchmark ejecutará la lógica real
    result = benchmark.pedantic(lambda: service.check_availability(table_id, ref_time, duration_hours=2.0),iterations=100, rounds=50)
    assert result is not None

@pytest.mark.benchmark(group="availability-check")
def test_benchmark_v3_availability(benchmark):
    service = setup_benchmark_service(V3Service, V3Repository, "bench_v3.db")
    
    table_id = list(service.tables.keys())[0]
    ref_time = datetime.datetime.now() + datetime.timedelta(days=1)
    
    result = benchmark.pedantic(lambda: service.check_availability(table_id, ref_time, duration_hours=2.0),iterations=100, rounds=50)
    assert result is not None