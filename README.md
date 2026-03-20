# Sistema de Reservas de Restaurante

Proyecto: implementación en Python de un sistema básico de reservas para un restaurante.

## Características

- Gestión de clientes: nombre, teléfono, email, historial de reservas
- Gestión de mesas: número, capacidad, zona (terraza/interior/privado)
- Reservas: crear, consultar, modificar, cancelar
- Validación de capacidad (no se acepta reserva para grupo mayor que capacidad de mesa)
- Comprobación de disponibilidad (superposición de franjas horarias)
- Recordatorios (reservas dentro de las próximas 24h)
- Estadísticas: mesa más reservada, hora punta, clientes frecuentes
- Persistencia con SQLite (`save_to_db`, `load_from_db`)
- Interfaz CLI y modo interactivo en terminal

## Archivos

- `restaurant_reservations.py`: lógica de negocio, persistencia y CLI/interactivo
- `test_restaurant_reservations.py`: pruebas con `pytest`

## Requisitos

- Python 3.8+
- `pytest` para tests

## Uso CLI

```bash
python restaurant_reservations.py add-customer "Ana" "123" "ana@mail.com"
python restaurant_reservations.py add-table 1 4 interior
python restaurant_reservations.py create-reservation "ana@mail.com" 1 2026-03-21T20:00 4 2
python restaurant_reservations.py list-reservations active
```

## Uso modo interactivo

```bash
python restaurant_reservations.py
```

Se mostrará un menú en terminal para crear clientes, mesas, reservas y ver estadísticas.

## Tests

```bash
pytest -q
```
