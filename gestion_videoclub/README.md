# Gestión de Videoclub

Proyecto de para gestionar un videoclub en Python con:
- Películas
- Clientes
- Alquileres
- Multas por devolución tardía

> Se usa como referencia principal la carpeta `src_refactorizar` (refactorizada y actualizada), la carpeta `src` se ha quedado desactualizada al refactorizar.

## Estructura del proyecto

- `src_refactorizar/`
  - `main.py`: punto de entrada (`python -m src_refactorizar.main`).
  - `database/db_handler.py`: gestión de SQLite, creación de tablas y conexión con context manager.
  - `models/`: modelo de datos (`Pelicula`, `Cliente`, `Alquiler`, `Multa`).
  - `services/`: lógica de negocio y acceso a datos (alquiler, multas, catálogo, clientes).
  - `ui/menu.py`: interfaz de consola con opciones de menú.
- `src_refactorizar/test/`: tests unitarios con `pytest`.

## Requisitos

- Python 3.10+
- pytest (solo para tests)

Instalación de dependencias (entorno virtual recomendado):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
pip install pytest
```

## Uso

1. Crear tablas y ejecutar aplicación:

```bash
cd gestion_videoclub
python -m src_refactorizar.main
```

2. El menú permite:
- Ver catálogo de películas
- Ver clientes (historial)
- Alquilar película
- Devolver película

## Tests

Ejecutar tests:

```bash
cd gestion_videoclub
python -m pytest -q src_refactorizar/test
```

Todos los tests deben pasar:
- `test_catalog_and_customer.py`
- `test_rental_and_penalty.py`

## Notas de implementación

- DB local `video_club.db` (o temporal en tests).
- La lógica de multas se calcula por días de retraso:
  - `Alquiler.calcular_multa_actual()` calcula retardo con `TARIFA_DIARIA_RETRASO`.
- `penalty_service` registra multas solo si monto > 0.
- Refactor: separación de responsabilidades (SRP) y servicios desacoplados.

## Siguiente evolución posible

- CRUD de películas/clientes
- Reportes de alquileres, multas y estado stock
- Saldos y pago de multas
- Persistencia con ORM (SQLAlchemy)
- UI gráfica o API REST
