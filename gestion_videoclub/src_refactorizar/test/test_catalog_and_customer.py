from src_refactorizar.database import db_handler
from src_refactorizar.services.catalog_service import CatalogService
from src_refactorizar.services.customer_service import CustomerService


def seed_samples():
    with db_handler.db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO peliculas (titulo, director, copias_disponibles) VALUES (?, ?, ?)",
                       ("Pelicula de prueba", "Director X", 3))
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                       ("Cliente Uno", "cliente1@mail.com"))
        conn.commit()


def test_listar_peliculas_vacia_por_defecto():
    peliculas = CatalogService.listar_peliculas()
    assert isinstance(peliculas, list)
    assert peliculas == []


def test_listar_peliculas_con_datos():
    seed_samples()
    peliculas = CatalogService.listar_peliculas()
    assert len(peliculas) == 1
    assert peliculas[0]["titulo"] == "Pelicula de prueba"


def test_listar_clientes_vacio():
    clientes = CustomerService.listar_clientes()
    assert clientes == []


def test_listar_clientes_con_datos():
    seed_samples()
    clientes = CustomerService.listar_clientes()
    assert len(clientes) == 1
    assert clientes[0]["nombre"] == "Cliente Uno"
