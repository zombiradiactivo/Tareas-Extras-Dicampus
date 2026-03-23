from __future__ import annotations

import datetime
import sqlite3
from pathlib import Path
from typing import Dict, Optional, Tuple

from .models import Customer, Reservation, Table, ReservationError


def _sanitize_db_path(db_value: str) -> Path:
    base_dir = Path.cwd().resolve() / "db"
    base_dir.mkdir(parents=True, exist_ok=True)

    path = Path(db_value)
    if path.is_absolute() or ".." in path.parts:
        raise ReservationError("Ruta de base de datos no permitida")

    target = (base_dir / path.name).resolve()
    if not str(target).startswith(str(base_dir)):
        raise ReservationError("Ruta de base de datos no permitida")

    return target


class ReservationRepository:
    def __init__(self, db_file: str = "reservations.db"):
        self.db_path = _sanitize_db_path(db_file)
        self._ensure_schema()

    def _ensure_schema(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tables (
                    table_id TEXT PRIMARY KEY,
                    number INTEGER,
                    capacity INTEGER,
                    zone TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id TEXT PRIMARY KEY,
                    customer_id TEXT,
                    table_id TEXT,
                    start TEXT,
                    end TEXT,
                    party_size INTEGER,
                    status TEXT
                )
                """
            )
            conn.commit()

    def load_all(self) -> Tuple[Dict[str, Customer], Dict[str, Table], Dict[str, Reservation]]:
        customers: Dict[str, Customer] = {}
        tables: Dict[str, Table] = {}
        reservations: Dict[str, Reservation] = {}

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()

            cur.execute("SELECT customer_id, name, phone, email FROM customers")
            for cid, name, phone, email in cur.fetchall():
                customers[cid] = Customer(name=name, phone=phone, email=email, customer_id=cid)

            cur.execute("SELECT table_id, number, capacity, zone FROM tables")
            for tid, number, capacity, zone in cur.fetchall():
                tables[tid] = Table(number=number, capacity=capacity, zone=zone, table_id=tid)

            cur.execute(
                "SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations"
            )
            for rid, cid, tid, start, end, party_size, status in cur.fetchall():
                reservations[rid] = Reservation(
                    reservation_id=rid,
                    customer_id=cid,
                    table_id=tid,
                    start=datetime.datetime.fromisoformat(start),
                    end=datetime.datetime.fromisoformat(end),
                    party_size=party_size,
                    status=status,
                )

        return customers, tables, reservations

    def add_customer(self, customer: Customer) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO customers (customer_id, name, phone, email) VALUES (?, ?, ?, ?)",
                (customer.customer_id, customer.name, customer.phone, customer.email),
            )
            conn.commit()

    def add_table(self, table: Table) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tables (table_id, number, capacity, zone) VALUES (?, ?, ?, ?)",
                (table.table_id, table.number, table.capacity, table.zone),
            )
            conn.commit()

    def add_reservation(self, reservation: Reservation) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reservations (reservation_id, customer_id, table_id, start, end, party_size, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    reservation.reservation_id,
                    reservation.customer_id,
                    reservation.table_id,
                    reservation.start.isoformat(),
                    reservation.end.isoformat(),
                    reservation.party_size,
                    reservation.status,
                ),
            )
            conn.commit()

    def update_reservation(self, reservation: Reservation) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE reservations SET customer_id=?, table_id=?, start=?, end=?, party_size=?, status=? WHERE reservation_id=?",
                (
                    reservation.customer_id,
                    reservation.table_id,
                    reservation.start.isoformat(),
                    reservation.end.isoformat(),
                    reservation.party_size,
                    reservation.status,
                    reservation.reservation_id,
                ),
            )
            conn.commit()

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT customer_id, name, phone, email FROM customers WHERE email=?", (email,))
            row = cur.fetchone()
            if row:
                return Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])

        return None
