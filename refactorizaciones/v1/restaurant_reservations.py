from __future__ import annotations

import argparse
import datetime
import hashlib
import sqlite3
import uuid
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAX_CUSTOMER_NAME = 100
MAX_CUSTOMER_PHONE = 20
MAX_CUSTOMER_EMAIL = 100
MAX_ZONE_LENGTH = 20
VALID_ZONES = {"terraza", "interior", "privado"}
DEFAULT_RESERVATION_DURATION_HOURS = 2.0
MAX_CACHE_RECORDS = 1000


@dataclass
class Customer:
    """Cliente que realiza reservas."""

    name: str
    phone: str
    email: str
    customer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reservation_ids: List[str] = field(default_factory=list)


@dataclass
class Table:
    """Mesa del restaurante."""

    number: int
    capacity: int
    zone: str
    table_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Reservation:
    """Reserva de una mesa por un cliente en una franja horaria determinada."""

    customer_id: str
    table_id: str
    start: datetime.datetime
    end: datetime.datetime
    party_size: int
    reservation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "active"


class ReservationError(Exception):
    """Excepción para errores de negocios en el sistema de reservas."""


class ReservationSystem:
    """Controlador de la lógica de reservas, mesas y clientes."""

    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.tables: Dict[str, Table] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.db_path: Optional[Path] = None
        self.max_cache_records = MAX_CACHE_RECORDS

    # ---------- Validaciones compartidas ----------
    @staticmethod
    def _normalize_text(value: str) -> str:
        return value.strip()

    def _validate_customer_data(self, name: str, phone: str, email: str):
        name = self._normalize_text(name)
        phone = self._normalize_text(phone)
        email = self._normalize_text(email)

        if not (name and phone and email):
            raise ReservationError("Nombre, teléfono y email son obligatorios")

        if len(name) > MAX_CUSTOMER_NAME or len(phone) > MAX_CUSTOMER_PHONE or len(email) > MAX_CUSTOMER_EMAIL:
            raise ReservationError("Campos exceden longitud máxima aceptada")

        if any(c.email == email for c in self.customers.values()):
            raise ReservationError("Email ya registrado")

        return name, phone, email

    def _check_zone(self, zone: str) -> str:
        normalized = self._normalize_text(zone).lower()
        if len(normalized) > MAX_ZONE_LENGTH:
            raise ReservationError("Zona excede longitud máxima")

        if normalized not in VALID_ZONES:
            raise ReservationError("Zona debe ser terraza, interior o privado")

        return normalized

    @staticmethod
    def _format_datetime(value: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(value)

    # ---------- Clientes ----------
    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        name, phone, email = self._validate_customer_data(name, phone, email)

        customer = Customer(name=name, phone=phone, email=email)
        self.customers[customer.customer_id] = customer
        return customer

    def _fetch_customer_from_db(self, customer_id: str) -> Optional[Customer]:
        if not self.db_path:
            return None

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT customer_id, name, phone, email FROM customers WHERE customer_id=?",
                (customer_id,),
            )
            row = cur.fetchone()

        if not row:
            return None

        return Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])

    def get_customer(self, customer_id: str) -> Customer:
        if customer_id in self.customers:
            return self.customers[customer_id]

        customer = self._fetch_customer_from_db(customer_id)
        if customer:
            self.customers[customer_id] = customer
            return customer

        raise ReservationError("Cliente no encontrado")

    def get_customer_by_email(self, email: str) -> Customer:
        email = self._normalize_text(email)

        for customer in self.customers.values():
            if customer.email == email:
                return customer

        if not self.db_path:
            raise ReservationError("Cliente no encontrado")

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT customer_id, name, phone, email FROM customers WHERE email=?",
                (email,),
            )
            row = cur.fetchone()

        if row:
            customer = Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])
            self.customers[row[0]] = customer
            return customer

        raise ReservationError("Cliente no encontrado")

    def get_customer_history(self, customer_id: str) -> List[Reservation]:
        customer = self.get_customer(customer_id)
        return [
            self.reservations[rid]
            for rid in customer.reservation_ids
            if rid in self.reservations
        ]

    # ---------- Mesas ----------
    def add_table(self, number: int, capacity: int, zone: str) -> Table:
        if number <= 0 or capacity <= 0:
            raise ReservationError("Número y capacidad de mesa deben ser mayores que 0")

        normalized_zone = self._check_zone(zone)

        if any(t.number == number for t in self.tables.values()):
            raise ReservationError("Número de mesa ya existe")

        table = Table(number=number, capacity=capacity, zone=normalized_zone)
        self.tables[table.table_id] = table
        return table

    def _fetch_table_from_db(self, table_id: str) -> Optional[Table]:
        if not self.db_path:
            return None

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT table_id, number, capacity, zone FROM tables WHERE table_id=?",
                (table_id,),
            )
            row = cur.fetchone()

        if not row:
            return None

        return Table(number=row[1], capacity=row[2], zone=row[3], table_id=row[0])

    def get_table(self, table_id: str) -> Table:
        if table_id in self.tables:
            return self.tables[table_id]

        table = self._fetch_table_from_db(table_id)
        if table:
            self.tables[table_id] = table
            return table

        raise ReservationError("Mesa no encontrada")

    # ---------- Reservas ----------
    @staticmethod
    def _assert_future_datetime(start: datetime.datetime):
        now = datetime.datetime.now()
        if start < now:
            raise ReservationError("La fecha y hora de la reserva debe ser en el futuro")

    @staticmethod
    def _is_overlapping(
        start1: datetime.datetime,
        end1: datetime.datetime,
        start2: datetime.datetime,
        end2: datetime.datetime,
    ) -> bool:
        return start1 < end2 and start2 < end1

    def _assert_party_size(self, party_size: int, table: Table):
        if party_size <= 0:
            raise ReservationError("Tamaño de grupo debe ser mayor que 0")

        if party_size > table.capacity:
            raise ReservationError("El número de personas excede la capacidad de la mesa")

    def check_availability(
        self,
        table_id: str,
        start: datetime.datetime,
        duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS,
        exclude_reservation_id: Optional[str] = None,
    ) -> bool:
        self.get_table(table_id)
        if duration_hours <= 0:
            raise ReservationError("Duración inválida")

        end = start + datetime.timedelta(hours=duration_hours)

        for res in self.reservations.values():
            if res.table_id != table_id or res.status != "active":
                continue

            if exclude_reservation_id and res.reservation_id == exclude_reservation_id:
                continue

            if self._is_overlapping(res.start, res.end, start, end):
                return False

        return True

    def create_reservation(
        self,
        customer_id: str,
        table_id: str,
        start: datetime.datetime,
        party_size: int = 1,
        duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS,
    ) -> Reservation:
        if customer_id not in self.customers:
            raise ReservationError("Cliente no registrado")

        table = self.get_table(table_id)
        self._assert_future_datetime(start)
        self._assert_party_size(party_size, table)

        if not self.check_availability(table_id, start, duration_hours):
            raise ReservationError("La mesa no está disponible en ese horario")

        reservation = Reservation(
            customer_id=customer_id,
            table_id=table_id,
            start=start,
            end=start + datetime.timedelta(hours=duration_hours),
            party_size=party_size,
        )

        self.reservations[reservation.reservation_id] = reservation
        self.customers[customer_id].reservation_ids.append(reservation.reservation_id)
        return reservation

    def _fetch_reservation_from_db(self, reservation_id: str) -> Optional[Reservation]:
        if not self.db_path:
            return None

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations WHERE reservation_id=?",
                (reservation_id,),
            )
            row = cur.fetchone()

        if not row:
            return None

        return Reservation(
            reservation_id=row[0],
            customer_id=row[1],
            table_id=row[2],
            start=datetime.datetime.fromisoformat(row[3]),
            end=datetime.datetime.fromisoformat(row[4]),
            party_size=row[5],
            status=row[6],
        )

    def get_reservation(self, reservation_id: str) -> Reservation:
        if reservation_id in self.reservations:
            return self.reservations[reservation_id]

        reservation = self._fetch_reservation_from_db(reservation_id)
        if reservation:
            self.reservations[reservation_id] = reservation
            return reservation

        raise ReservationError("Reserva no encontrada")

    def modify_reservation(
        self,
        reservation_id: str,
        table_id: Optional[str] = None,
        start: Optional[datetime.datetime] = None,
        party_size: Optional[int] = None,
        duration_hours: Optional[float] = None,
    ) -> Reservation:
        reservation = self.get_reservation(reservation_id)
        if reservation.status != "active":
            raise ReservationError("Solo se pueden modificar reservas activas")

        new_table_id = table_id or reservation.table_id
        new_start = start or reservation.start
        new_party_size = party_size if party_size is not None else reservation.party_size
        new_duration = (
            duration_hours
            if duration_hours is not None
            else (reservation.end - reservation.start).total_seconds() / 3600
        )

        table = self.get_table(new_table_id)
        self._assert_future_datetime(new_start)
        self._assert_party_size(new_party_size, table)

        if not self.check_availability(new_table_id, new_start, new_duration, exclude_reservation_id=reservation_id):
            raise ReservationError("Horario no disponible para la mesa solicitada")

        reservation.table_id = new_table_id
        reservation.start = new_start
        reservation.end = new_start + datetime.timedelta(hours=new_duration)
        reservation.party_size = new_party_size
        return reservation

    def cancel_reservation(self, reservation_id: str) -> Reservation:
        reservation = self.get_reservation(reservation_id)
        if reservation.status == "cancelled":
            raise ReservationError("Reserva ya cancelada")

        reservation.status = "cancelled"
        return reservation

    def list_reservations(self, status: Optional[str] = None) -> List[Reservation]:
        if self.db_path and len(self.reservations) < self.max_cache_records:
            query = "SELECT reservation_id FROM reservations"
            params = ()

            if status:
                query += " WHERE status=?"
                params = (status,)

            query += " LIMIT ?"
            params += (self.max_cache_records,)

            with sqlite3.connect(str(self.db_path)) as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                rows = cur.fetchall()

            return [self.get_reservation(rid) for (rid,) in rows]

        if status is None:
            return list(self.reservations.values())

        return [r for r in self.reservations.values() if r.status == status]

    def find_reservations_by_date(self, date: datetime.date) -> List[Reservation]:
        return [
            r
            for r in self.reservations.values()
            if r.status == "active" and r.start.date() == date
        ]

    def is_table_available(
        self,
        table_id: str,
        start: datetime.datetime,
        duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS,
    ) -> bool:
        return self.check_availability(table_id, start, duration_hours)

    def upcoming_reminders(self, reference: Optional[datetime.datetime] = None) -> List[Reservation]:
        now = reference or datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [
            r
            for r in self.reservations.values()
            if r.status == "active" and now <= r.start <= limit
        ]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self) -> Optional[Tuple[Table, int]]:
        counter = Counter(r.table_id for r in self.reservations.values() if r.status == "active")
        if not counter:
            return None

        table_id, count = counter.most_common(1)[0]
        table = self.tables.get(table_id)
        if table is None:
            return None

        return table, count


    def peak_hour(self) -> Optional[Tuple[int, int]]:
        hour_counts = Counter(r.start.hour for r in self.reservations.values() if r.status == "active")
        if not hour_counts:
            return None

        hour, count = hour_counts.most_common(1)[0]
        return hour, count

    def frequent_clients(self, top_n: int = 3) -> List[Tuple[Customer, int]]:
        customer_counts = Counter(r.customer_id for r in self.reservations.values() if r.status == "active")
        most_common = customer_counts.most_common(top_n)
        return [(self.customers[cid], count) for cid, count in most_common if cid in self.customers]

    def save_to_db(self, path: str):
        db_path = Path(path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(str(db_path)) as conn:
            cur = conn.cursor()
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT
            )'''
            )
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS tables (
                table_id TEXT PRIMARY KEY,
                number INTEGER,
                capacity INTEGER,
                zone TEXT
            )'''
            )
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS reservations (
                reservation_id TEXT PRIMARY KEY,
                customer_id TEXT,
                table_id TEXT,
                start TEXT,
                end TEXT,
                party_size INTEGER,
                status TEXT
            )'''
            )

            cur.execute("DELETE FROM reservations")
            cur.execute("DELETE FROM customers")
            cur.execute("DELETE FROM tables")

            for c in self.customers.values():
                cur.execute(
                    "INSERT INTO customers (customer_id, name, phone, email) VALUES (?, ?, ?, ?)",
                    (c.customer_id, c.name, c.phone, c.email),
                )

            for t in self.tables.values():
                cur.execute(
                    "INSERT INTO tables (table_id, number, capacity, zone) VALUES (?, ?, ?, ?)",
                    (t.table_id, t.number, t.capacity, t.zone),
                )

            for r in self.reservations.values():
                cur.execute(
                    "INSERT INTO reservations (reservation_id, customer_id, table_id, start, end, party_size, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        r.reservation_id,
                        r.customer_id,
                        r.table_id,
                        r.start.isoformat(),
                        r.end.isoformat(),
                        r.party_size,
                        r.status,
                    ),
                )

            conn.commit()

        self.db_path = db_path

    def load_from_db(self, path: str, max_rows: int = MAX_CACHE_RECORDS):
        self.db_path = Path(path).resolve()
        self.customers = {}
        self.tables = {}
        self.reservations = {}

        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()

            cur.execute('SELECT customer_id, name, phone, email FROM customers LIMIT ?', (max_rows,))
            for row in cur.fetchall():
                self.customers[row[0]] = Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])

            cur.execute('SELECT table_id, number, capacity, zone FROM tables LIMIT ?', (max_rows,))
            for row in cur.fetchall():
                self.tables[row[0]] = Table(number=row[1], capacity=row[2], zone=row[3], table_id=row[0])

            cur.execute(
                'SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations LIMIT ?',
                (max_rows,),
            )
            for row in cur.fetchall():
                self.reservations[row[0]] = Reservation(
                    customer_id=row[1],
                    table_id=row[2],
                    start=datetime.datetime.fromisoformat(row[3]),
                    end=datetime.datetime.fromisoformat(row[4]),
                    party_size=row[5],
                    reservation_id=row[0],
                    status=row[6],
                )

        for customer in self.customers.values():
            customer.reservation_ids = [
                r.reservation_id for r in self.reservations.values() if r.customer_id == customer.customer_id
            ]


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


def format_public_id(expensive_id: str) -> str:
    return hashlib.sha256(expensive_id.encode()).hexdigest()[:10]


def main():
    parser = argparse.ArgumentParser(description="Sistema básico de reservas para restaurante")
    parser.add_argument("--db", default="reservations.db", help="Ruta de la base de datos SQLite")
    subparsers = parser.add_subparsers(dest="command")

    parser_add_customer = subparsers.add_parser("add-customer")
    parser_add_customer.add_argument("name")
    parser_add_customer.add_argument("phone")
    parser_add_customer.add_argument("email")

    parser_add_table = subparsers.add_parser("add-table")
    parser_add_table.add_argument("number", type=int)
    parser_add_table.add_argument("capacity", type=int)
    parser_add_table.add_argument("zone")

    parser_create = subparsers.add_parser("create-reservation")
    parser_create.add_argument("customer_email")
    parser_create.add_argument("table_number", type=int)
    parser_create.add_argument("start", help="YYYY-MM-DDTHH:MM")
    parser_create.add_argument("party_size", type=int)
    parser_create.add_argument("duration", type=float, default=DEFAULT_RESERVATION_DURATION_HOURS)

    parser_list = subparsers.add_parser("list-reservations")
    parser_list.add_argument("status", nargs="?", choices=["active", "cancelled"], default=None)

    args = parser.parse_args()

    if args.command == "add-customer":
        if len(args.name) > MAX_CUSTOMER_NAME or len(args.phone) > MAX_CUSTOMER_PHONE or len(args.email) > MAX_CUSTOMER_EMAIL:
            raise ReservationError("Valores demasiado largos")

    if args.command == "add-table":
        if len(args.zone) > MAX_ZONE_LENGTH:
            raise ReservationError("Valor de zona demasiado largo")

    if args.command == "create-reservation":
        if len(args.customer_email) > MAX_CUSTOMER_EMAIL:
            raise ReservationError("Email demasiado largo")

    safe_db = _sanitize_db_path(args.db)
    db_path = str(safe_db)
    system = ReservationSystem()
    try:
        system.load_from_db(db_path)
    except Exception:
        pass

    if args.command == "add-customer":
        c = system.add_customer(args.name, args.phone, args.email)
        print(f"Cliente creado: {hashlib.sha256(c.customer_id.encode()).hexdigest()[:8]}")
        system.save_to_db(db_path)
    elif args.command == "add-table":
        t = system.add_table(args.number, args.capacity, args.zone)
        print(f"Mesa creada: {format_public_id(t.table_id)}")
        system.save_to_db(db_path)
    elif args.command == "create-reservation":
        customer = system.get_customer_by_email(args.customer_email)
        table = next((t for t in system.tables.values() if t.number == args.table_number), None)
        if table is None:
            raise ReservationError("Mesa no encontrada")

        start = datetime.datetime.fromisoformat(args.start)
        r = system.create_reservation(
            customer.customer_id,
            table.table_id,
            start,
            party_size=args.party_size,
            duration_hours=args.duration,
        )
        print(f"Reserva creada: {format_public_id(r.reservation_id)}")
        system.save_to_db(db_path)

    elif args.command == "list-reservations":
        lista = system.list_reservations(status=args.status)
        for r in lista:
            print(r)

    elif args.command is None:
        run_interactive_menu(system, db_path)
    else:
        parser.print_help()

    # Guardado final de seguridad (comando sin cambios no romperá el DB existente)
    system.save_to_db(db_path)


def run_interactive_menu(system: ReservationSystem, db_path: str):
    print("Sistema de Reservas - Modo Interactivo")
    print("Escribe el número que quieras ejecutar y presiona Enter")

    def get_date(prompt: str) -> datetime.datetime:
        while True:
            value = input(prompt).strip()
            try:
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                print("Fecha/hora en formato incorrecto. Usa YYYY-MM-DDTHH:MM")

    while True:
        print("\nOpciones:")
        print("1) Agregar cliente")
        print("2) Agregar mesa")
        print("3) Crear reserva")
        print("4) Listar reservas")
        print("5) Comprobar disponibilidad")
        print("6) Recordatorios (menos de 24h)")
        print("7) Estadísticas")
        print("8) Cancelar reserva")
        print("9) Modificar reserva")
        print("q) Salir")

        choice = input("Opción: ").strip().lower()
        if choice == "q":
            break

        try:
            if choice == "1":
                name = input("Nombre: ").strip()
                phone = input("Teléfono: ").strip()
                email = input("Email: ").strip()
                customer = system.add_customer(name, phone, email)
                print(f"Cliente creado: {format_public_id(customer.customer_id)}")
                system.save_to_db(db_path)

            elif choice == "2":
                number = int(input("Número de mesa: ").strip())
                capacity = int(input("Capacidad: ").strip())
                zone = input("Zona (terraza/interior/privado): ").strip()
                table = system.add_table(number, capacity, zone)
                print(f"Mesa creada: {format_public_id(table.table_id)}")
                system.save_to_db(db_path)

            elif choice == "3":
                email = input("Email del cliente: ").strip()
                customer = system.get_customer_by_email(email)
                table_num = int(input("Número de mesa: ").strip())
                table = next((t for t in system.tables.values() if t.number == table_num), None)
                if table is None:
                    raise ReservationError("Mesa no encontrada")
                start = get_date("Inicio (YYYY-MM-DDTHH:MM): ")
                party = int(input("Tamaño del grupo: ").strip())
                duration = float(input("Duración (horas, default 2): ").strip() or DEFAULT_RESERVATION_DURATION_HOURS)
                reservation = system.create_reservation(
                    customer.customer_id, table.table_id, start, party_size=party, duration_hours=duration
                )
                print(f"Reserva creada: {format_public_id(reservation.reservation_id)}")
                system.save_to_db(db_path)

            elif choice == "4":
                status = input("Estado (active/cancelled/empty): ").strip() or None
                if status == "empty":
                    status = None
                reservations = system.list_reservations(status=status)
                for r in reservations:
                    print(r)

            elif choice == "5":
                table_num = int(input("Número de mesa: ").strip())
                table = next((t for t in system.tables.values() if t.number == table_num), None)
                if table is None:
                    raise ReservationError("Mesa no encontrada")
                start = get_date("Inicio (YYYY-MM-DDTHH:MM): ")
                duration = float(input("Duración (horas, default 2): ").strip() or DEFAULT_RESERVATION_DURATION_HOURS)
                available = system.is_table_available(table.table_id, start, duration)
                print("Disponible" if available else "No disponible")

            elif choice == "6":
                reminders = system.upcoming_reminders()
                if reminders:
                    for r in reminders:
                        print(r)
                else:
                    print("No hay reservas dentro de 24 horas")

            elif choice == "7":
                m = system.most_reserved_table()
                p = system.peak_hour()
                f = system.frequent_clients(3)
                print(f"Mesa más reservada: {m}")
                print(f"Hora punta: {p}")
                print("Clientes frecuentes:")
                for customer, cnt in f:
                    print(f" {customer.name} ({customer.email}): {cnt}")

            elif choice == "8":
                reservation_id = input("ID de la reserva a cancelar: ").strip()
                reservation = system.cancel_reservation(reservation_id)
                print(f"Reserva cancelada: {format_public_id(reservation.reservation_id)}")
                system.save_to_db(db_path)

            elif choice == "9":
                reservation_id = input("ID de la reserva a modificar: ").strip()
                reservation = system.get_reservation(reservation_id)
                print(f"Reserva actual: {reservation}")

                new_table_number = input("Nuevo número de mesa (vacío para no cambiar): ").strip()
                if new_table_number:
                    table_num = int(new_table_number)
                    table = next((t for t in system.tables.values() if t.number == table_num), None)
                    if table is None:
                        raise ReservationError("Mesa no encontrada")
                    table_id = table.table_id
                else:
                    table_id = reservation.table_id

                new_start_text = input("Nueva fecha/hora (YYYY-MM-DDTHH:MM) (vacío para no cambiar): ").strip()
                new_start = get_date("Nueva fecha/hora (YYYY-MM-DDTHH:MM): ") if new_start_text else None

                new_party = input("Nuevo tamaño del grupo (vacío para no cambiar): ").strip()
                new_party_size = int(new_party) if new_party else None

                new_duration = input("Nueva duración (horas) (vacío para no cambiar): ").strip()
                new_duration = float(new_duration) if new_duration else None

                updated = system.modify_reservation(
                    reservation_id,
                    table_id=table_id,
                    start=new_start,
                    party_size=new_party_size,
                    duration_hours=new_duration,
                )
                print(f"Reserva modificada: {format_public_id(updated.reservation_id)}")
                system.save_to_db(db_path)

            else:
                print("Opción inválida")

        except ReservationError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Entrada inválida: {e}")

    print("Saliendo de la interfaz interactiva. Se guarda la base de datos.")


if __name__ == "__main__":
    main()
