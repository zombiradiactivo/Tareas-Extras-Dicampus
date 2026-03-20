from __future__ import annotations

import argparse
import datetime
import sqlite3
import uuid
from dataclasses import dataclass, field
from collections import Counter
from typing import Dict, List, Optional, Tuple


@dataclass
class Customer:
    name: str
    phone: str
    email: str
    customer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reservation_ids: List[str] = field(default_factory=list)


@dataclass
class Table:
    number: int
    capacity: int
    zone: str
    table_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Reservation:
    customer_id: str
    table_id: str
    start: datetime.datetime
    end: datetime.datetime
    party_size: int
    reservation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "active"


class ReservationError(Exception):
    pass


class ReservationSystem:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.tables: Dict[str, Table] = {}
        self.reservations: Dict[str, Reservation] = {}

    # ---------- Clientes ----------
    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        if not name.strip() or not phone.strip() or not email.strip():
            raise ReservationError("Nombre, teléfono y email son obligatorios")

        if any(c.email == email for c in self.customers.values()):
            raise ReservationError("Email ya registrado")

        customer = Customer(name=name.strip(), phone=phone.strip(), email=email.strip())
        self.customers[customer.customer_id] = customer
        return customer

    def get_customer(self, customer_id: str) -> Customer:
        try:
            return self.customers[customer_id]
        except KeyError:
            raise ReservationError("Cliente no encontrado")

    def get_customer_by_email(self, email: str) -> Customer:
        for customer in self.customers.values():
            if customer.email == email:
                return customer
        raise ReservationError("Cliente no encontrado")

    def get_customer_history(self, customer_id: str) -> List[Reservation]:
        customer = self.get_customer(customer_id)
        return [self.reservations[rid] for rid in customer.reservation_ids if rid in self.reservations]

    # ---------- Mesas ----------
    def add_table(self, number: int, capacity: int, zone: str) -> Table:
        if number <= 0 or capacity <= 0:
            raise ReservationError("Número y capacidad de mesa deben ser mayores que 0")

        normalized_zone = zone.strip().lower()
        if normalized_zone not in {"terraza", "interior", "privado"}:
            raise ReservationError("Zona debe ser terraza, interior o privado")

        if any(t.number == number for t in self.tables.values()):
            raise ReservationError("Número de mesa ya existe")

        table = Table(number=number, capacity=capacity, zone=normalized_zone)
        self.tables[table.table_id] = table
        return table

    def get_table(self, table_id: str) -> Table:
        try:
            return self.tables[table_id]
        except KeyError:
            raise ReservationError("Mesa no encontrada")

    # ---------- Reservas ----------
    @staticmethod
    def _assert_future_datetime(start: datetime.datetime):
        now = datetime.datetime.now()
        if start < now:
            raise ReservationError("La fecha y hora de la reserva debe ser en el futuro")

    @staticmethod
    def _is_overlapping(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime) -> bool:
        return start1 < end2 and start2 < end1

    def _assert_party_size(self, party_size: int, table: Table):
        if party_size <= 0:
            raise ReservationError("Tamaño de grupo debe ser mayor que 0")
        if party_size > table.capacity:
            raise ReservationError("El número de personas excede la capacidad de la mesa")

    def check_availability(self, table_id: str, start: datetime.datetime, duration_hours: float = 2.0, exclude_reservation_id: Optional[str] = None) -> bool:
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

    def create_reservation(self, customer_id: str, table_id: str, start: datetime.datetime, party_size: int = 1, duration_hours: float = 2.0) -> Reservation:
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

    def get_reservation(self, reservation_id: str) -> Reservation:
        try:
            return self.reservations[reservation_id]
        except KeyError:
            raise ReservationError("Reserva no encontrada")

    def modify_reservation(self, reservation_id: str, table_id: Optional[str] = None, start: Optional[datetime.datetime] = None, party_size: Optional[int] = None, duration_hours: Optional[float] = None) -> Reservation:
        reservation = self.get_reservation(reservation_id)
        if reservation.status != "active":
            raise ReservationError("Solo se pueden modificar reservas activas")

        new_table_id = table_id or reservation.table_id
        new_start = start or reservation.start
        new_party_size = party_size if party_size is not None else reservation.party_size
        new_duration = duration_hours if duration_hours is not None else (reservation.end - reservation.start).total_seconds() / 3600

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
        if status is None:
            return list(self.reservations.values())
        return [r for r in self.reservations.values() if r.status == status]

    def find_reservations_by_date(self, date: datetime.date) -> List[Reservation]:
        return [r for r in self.reservations.values() if r.start.date() == date and r.status == "active"]

    def is_table_available(self, table_id: str, start: datetime.datetime, duration_hours: float = 2.0) -> bool:
        return self.check_availability(table_id, start, duration_hours)

    def upcoming_reminders(self, reference: Optional[datetime.datetime] = None) -> List[Reservation]:
        now = reference or datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [r for r in self.reservations.values() if r.status == "active" and now <= r.start <= limit]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self) -> Optional[Tuple[Table, int]]:
        counter = Counter(r.table_id for r in self.reservations.values() if r.status == "active")
        if not counter:
            return None

        table_id, count = counter.most_common(1)[0]
        return self.tables[table_id], count

    def peak_hour(self) -> Optional[Tuple[int, int]]:
        hour_counts = Counter(r.start.hour for r in self.reservations.values() if r.status == "active")
        if not hour_counts:
            return None

        hour, count = hour_counts.most_common(1)[0]
        return hour, count

    def frequent_clients(self, top_n: int = 3) -> List[Tuple[Customer, int]]:
        customer_counts = Counter(r.customer_id for r in self.reservations.values() if r.status == "active")
        most_common = customer_counts.most_common(top_n)
        return [(self.customers[cid], count) for cid, count in most_common]

    def save_to_db(self, path: str):
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS tables (
            table_id TEXT PRIMARY KEY,
            number INTEGER,
            capacity INTEGER,
            zone TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS reservations (
            reservation_id TEXT PRIMARY KEY,
            customer_id TEXT,
            table_id TEXT,
            start TEXT,
            end TEXT,
            party_size INTEGER,
            status TEXT
        )''')

        cur.execute('DELETE FROM reservations')
        cur.execute('DELETE FROM customers')
        cur.execute('DELETE FROM tables')

        for c in self.customers.values():
            cur.execute('INSERT INTO customers (customer_id, name, phone, email) VALUES (?, ?, ?, ?)', (c.customer_id, c.name, c.phone, c.email))

        for t in self.tables.values():
            cur.execute('INSERT INTO tables (table_id, number, capacity, zone) VALUES (?, ?, ?, ?)', (t.table_id, t.number, t.capacity, t.zone))

        for r in self.reservations.values():
            cur.execute(
                'INSERT INTO reservations (reservation_id, customer_id, table_id, start, end, party_size, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (r.reservation_id, r.customer_id, r.table_id, r.start.isoformat(), r.end.isoformat(), r.party_size, r.status),
            )

        conn.commit()
        conn.close()

    def load_from_db(self, path: str):
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        cur.execute('SELECT customer_id, name, phone, email FROM customers')
        self.customers = {row[0]: Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0]) for row in cur.fetchall()}

        cur.execute('SELECT table_id, number, capacity, zone FROM tables')
        self.tables = {row[0]: Table(number=row[1], capacity=row[2], zone=row[3], table_id=row[0]) for row in cur.fetchall()}

        cur.execute('SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations')
        self.reservations = {}
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
            customer.reservation_ids = [r.reservation_id for r in self.reservations.values() if r.customer_id == customer.customer_id]

        conn.close()


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
    parser_create.add_argument("duration", type=float, default=2.0)

    parser_list = subparsers.add_parser("list-reservations")
    parser_list.add_argument("status", nargs="?", choices=["active", "cancelled"], default=None)

    args = parser.parse_args()

    system = ReservationSystem()
    try:
        system.load_from_db(args.db)
    except Exception:
        pass

    if args.command == "add-customer":
        c = system.add_customer(args.name, args.phone, args.email)
        print(f"Cliente creado: {c.customer_id}")
    elif args.command == "add-table":
        t = system.add_table(args.number, args.capacity, args.zone)
        print(f"Mesa creada: {t.table_id}")
    elif args.command == "create-reservation":
        customer = system.get_customer_by_email(args.customer_email)
        table = next((t for t in system.tables.values() if t.number == args.table_number), None)
        if table is None:
            raise ReservationError("Mesa no encontrada")
        start = datetime.datetime.fromisoformat(args.start)
        r = system.create_reservation(customer.customer_id, table.table_id, start, party_size=args.party_size, duration_hours=args.duration)
        print(f"Reserva creada: {r.reservation_id}")
    elif args.command == "list-reservations":
        lista = system.list_reservations(status=args.status)
        for r in lista:
            print(r)
    elif args.command is None:
        run_interactive_menu(system)
    else:
        parser.print_help()

    system.save_to_db(args.db)


def run_interactive_menu(system: ReservationSystem):
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
                print(f"Cliente creado: {customer.customer_id}")

            elif choice == "2":
                number = int(input("Número de mesa: ").strip())
                capacity = int(input("Capacidad: ").strip())
                zone = input("Zona (terraza/interior/privado): ").strip()
                table = system.add_table(number, capacity, zone)
                print(f"Mesa creada: {table.table_id}")

            elif choice == "3":
                email = input("Email del cliente: ").strip()
                customer = system.get_customer_by_email(email)
                table_num = int(input("Número de mesa: ").strip())
                table = next((t for t in system.tables.values() if t.number == table_num), None)
                if table is None:
                    raise ReservationError("Mesa no encontrada")
                start = get_date("Inicio (YYYY-MM-DDTHH:MM): ")
                party = int(input("Tamaño del grupo: ").strip())
                duration = float(input("Duración (horas, default 2): ").strip() or 2)
                reservation = system.create_reservation(customer.customer_id, table.table_id, start, party_size=party, duration_hours=duration)
                print(f"Reserva creada: {reservation.reservation_id}")

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
                duration = float(input("Duración (horas, default 2): ").strip() or 2)
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

            else:
                print("Opción inválida")

        except ReservationError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Entrada inválida: {e}")

    print("Saliendo de la interfaz interactiva. Se guarda la base de datos.")


if __name__ == "__main__":
    main()

