from __future__ import annotations

import argparse
import datetime
import hashlib
import sqlite3
import uuid
from dataclasses import dataclass, field
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple


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
        self.max_cache_records = 1000  # evitan carga excesiva de memoria

    # ---------- Clientes ----------
    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        """Agrega un cliente y devuelve el objeto creado.

        Lanza ReservationError si los datos están incompletos o el email ya existe.
        """

        if not name.strip() or not phone.strip() or not email.strip():
            raise ReservationError("Nombre, teléfono y email son obligatorios")

        if len(name) > 100 or len(phone) > 20 or len(email) > 100:
            raise ReservationError("Campos exceden longitud máxima aceptada")

        if any(c.email == email for c in self.customers.values()):
            raise ReservationError("Email ya registrado")

        customer = Customer(name=name.strip(), phone=phone.strip(), email=email.strip())
        self.customers[customer.customer_id] = customer
        return customer

    def _fetch_customer_from_db(self, customer_id: str) -> Optional[Customer]:
        if not self.db_path:
            return None
        with sqlite3.connect(str(self.db_path)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT customer_id, name, phone, email FROM customers WHERE customer_id=?', (customer_id,))
            row = cur.fetchone()
            if row:
                return Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])
        return None

    def get_customer(self, customer_id: str) -> Customer:
        """Devuelve un cliente por ID. Lanza ReservationError si no existe."""
        if customer_id in self.customers:
            return self.customers[customer_id]

        persistent = self._fetch_customer_from_db(customer_id)
        if persistent:
            self.customers[customer_id] = persistent
            return persistent

        raise ReservationError("Cliente no encontrado")

    def get_customer_by_email(self, email: str) -> Customer:
        """Busca un cliente por email. Lanza ReservationError si no existe."""
        for customer in self.customers.values():
            if customer.email == email:
                return customer

        if self.db_path:
            with sqlite3.connect(str(self.db_path)) as conn:
                cur = conn.cursor()
                cur.execute('SELECT customer_id, name, phone, email FROM customers WHERE email=?', (email,))
                row = cur.fetchone()
                if row:
                    customer = Customer(name=row[1], phone=row[2], email=row[3], customer_id=row[0])
                    self.customers[row[0]] = customer
                    return customer

        raise ReservationError("Cliente no encontrado")

    def get_customer_history(self, customer_id: str) -> List[Reservation]:
        """Retorna todas las reservas asociadas a un cliente."""
        customer = self.get_customer(customer_id)
        return [self.reservations[rid] for rid in customer.reservation_ids if rid in self.reservations]

    # ---------- Mesas ----------
    def add_table(self, number: int, capacity: int, zone: str) -> Table:
        """Registra una nueva mesa en el sistema."""
        if number <= 0 or capacity <= 0:
            raise ReservationError("Número y capacidad de mesa deben ser mayores que 0")

        if len(zone.strip()) > 20:
            raise ReservationError("Zona excede longitud máxima")

        normalized_zone = zone.strip().lower()
        if normalized_zone not in {"terraza", "interior", "privado"}:
            raise ReservationError("Zona debe ser terraza, interior o privado")

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
            cur.execute('SELECT table_id, number, capacity, zone FROM tables WHERE table_id=?', (table_id,))
            row = cur.fetchone()
            if row:
                return Table(number=row[1], capacity=row[2], zone=row[3], table_id=row[0])
        return None

    def get_table(self, table_id: str) -> Table:
        """Devuelve una mesa por ID. Lanza ReservationError si no existe."""
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
        """Verifica que la fecha de inicio sea en el futuro."""
        now = datetime.datetime.now()
        if start < now:
            raise ReservationError("La fecha y hora de la reserva debe ser en el futuro")

    @staticmethod
    def _is_overlapping(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime) -> bool:
        """Determina si dos intervalos de tiempo se solapan."""
        return start1 < end2 and start2 < end1

    def _assert_party_size(self, party_size: int, table: Table):
        """Verifica que el tamaño del grupo sea adecuado para la mesa."""
        if party_size <= 0:
            raise ReservationError("Tamaño de grupo debe ser mayor que 0")
        if party_size > table.capacity:
            raise ReservationError("El número de personas excede la capacidad de la mesa")

    def check_availability(self, table_id: str, start: datetime.datetime, duration_hours: float = 2.0, exclude_reservation_id: Optional[str] = None) -> bool:
        """Comprueba si una mesa está libre para una franja horaria dada."""
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
        """Crea una reserva nueva.

        Valida cliente, mesa, tiempo futuro, tamaño de grupo y disponibilidad.
        """
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
            cur.execute('SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations WHERE reservation_id=?', (reservation_id,))
            row = cur.fetchone()
            if row:
                return Reservation(
                    reservation_id=row[0],
                    customer_id=row[1],
                    table_id=row[2],
                    start=datetime.datetime.fromisoformat(row[3]),
                    end=datetime.datetime.fromisoformat(row[4]),
                    party_size=row[5],
                    status=row[6],
                )
        return None

    def get_reservation(self, reservation_id: str) -> Reservation:
        """Recupera una reserva por ID. Lanza error si no existe."""
        if reservation_id in self.reservations:
            return self.reservations[reservation_id]

        reservation = self._fetch_reservation_from_db(reservation_id)
        if reservation:
            self.reservations[reservation_id] = reservation
            return reservation

        raise ReservationError("Reserva no encontrada")

    def modify_reservation(self, reservation_id: str, table_id: Optional[str] = None, start: Optional[datetime.datetime] = None, party_size: Optional[int] = None, duration_hours: Optional[float] = None) -> Reservation:
        """Modifica los datos de una reserva activa."""
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
        """Cancela una reserva activa."""
        reservation = self.get_reservation(reservation_id)
        if reservation.status == "cancelled":
            raise ReservationError("Reserva ya cancelada")

        reservation.status = "cancelled"
        return reservation

    def list_reservations(self, status: Optional[str] = None) -> List[Reservation]:
        """Lista reservas, opcionalmente filtrando por estado."""
        if self.db_path and len(self.reservations) < self.max_cache_records:
            with sqlite3.connect(str(self.db_path)) as conn:
                cur = conn.cursor()
                if status:
                    cur.execute('SELECT reservation_id FROM reservations WHERE status=? LIMIT ?', (status, self.max_cache_records))
                else:
                    cur.execute('SELECT reservation_id FROM reservations LIMIT ?', (self.max_cache_records,))
                rows = cur.fetchall()
            res = []
            for (rid,) in rows:
                res.append(self.get_reservation(rid))
            return res

        if status is None:
            return list(self.reservations.values())
        return [r for r in self.reservations.values() if r.status == status]

    def find_reservations_by_date(self, date: datetime.date) -> List[Reservation]:
        """Devuelve reservas activas de un día determinado."""
        return [r for r in self.reservations.values() if r.start.date() == date and r.status == "active"]

    def is_table_available(self, table_id: str, start: datetime.datetime, duration_hours: float = 2.0) -> bool:
        """Alias del método de comprobación de disponibilidad."""
        return self.check_availability(table_id, start, duration_hours)

    def upcoming_reminders(self, reference: Optional[datetime.datetime] = None) -> List[Reservation]:
        """Devuelve reservas activas que comienzan en las próximas 24 horas."""
        now = reference or datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [r for r in self.reservations.values() if r.status == "active" and now <= r.start <= limit]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self) -> Optional[Tuple[Table, int]]:
        """Retorna la mesa más reservada y su número de reservas."""
        counter = Counter(r.table_id for r in self.reservations.values() if r.status == "active")
        if not counter:
            return None

        table_id, count = counter.most_common(1)[0]
        return self.tables[table_id], count

    def peak_hour(self) -> Optional[Tuple[int, int]]:
        """Determina la hora del día con más reservas activas."""
        hour_counts = Counter(r.start.hour for r in self.reservations.values() if r.status == "active")
        if not hour_counts:
            return None

        hour, count = hour_counts.most_common(1)[0]
        return hour, count

    def frequent_clients(self, top_n: int = 3) -> List[Tuple[Customer, int]]:
        """Devuelve los clientes con más reservas activas, ordenados de mayor a menor."""
        customer_counts = Counter(r.customer_id for r in self.reservations.values() if r.status == "active")
        most_common = customer_counts.most_common(top_n)
        return [(self.customers[cid], count) for cid, count in most_common]

    def save_to_db(self, path: str):
        """Guarda el estado actual en una base de datos SQLite.

        Usa siempre consultas parametrizadas para mitigar riesgos de SQLi.
        """
        db_path = Path(path).resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(db_path)) as conn:
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
        self.db_path = db_path

    def load_from_db(self, path: str, max_rows: int = 1000):
        """Carga datos desde una base de datos SQLite al sistema en memoria.

        Para evitar DoS por memoria, carga solo un límite de filas en caché.
        En su lugar, métodos de acceso recuperan de la DB bajo demanda.
        """
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

            cur.execute('SELECT reservation_id, customer_id, table_id, start, end, party_size, status FROM reservations LIMIT ?', (max_rows,))
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


def _sanitize_db_path(db_value: str) -> Path:
    """Restringe la ruta del DB a un directorio seguro para prevenir path traversal."""
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
    """Genera una versión no reversible corta para presentaciones seguras."""
    return hashlib.sha256(expensive_id.encode()).hexdigest()[:10]


def main():
    """Entry point CLI: ejecuta comandos o modo interactivo."""
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

    # Validación de parámetros de cmdline para evitar datos extremos
    if args.command == "add-customer":
        if len(args.name) > 100 or len(args.phone) > 20 or len(args.email) > 100:
            raise ReservationError("Valores demasiado largos")
    if args.command == "add-table":
        if len(args.zone) > 20:
            raise ReservationError("Valor de zona demasiado largo")
    if args.command == "create-reservation":
        if len(args.customer_email) > 100:
            raise ReservationError("Email demasiado largo")

    safe_db = _sanitize_db_path(args.db)
    system = ReservationSystem()
    try:
        system.load_from_db(str(safe_db))
    except Exception:
        pass

    if args.command == "add-customer":
        c = system.add_customer(args.name, args.phone, args.email)
        print(f"Cliente creado: {hashlib.sha256(c.customer_id.encode()).hexdigest()[:8]}")
    elif args.command == "add-table":
        t = system.add_table(args.number, args.capacity, args.zone)
        print(f"Mesa creada: {format_public_id(t.table_id)}")
    elif args.command == "create-reservation":
        customer = system.get_customer_by_email(args.customer_email)
        table = next((t for t in system.tables.values() if t.number == args.table_number), None)
        if table is None:
            raise ReservationError("Mesa no encontrada")
        start = datetime.datetime.fromisoformat(args.start)
        r = system.create_reservation(customer.customer_id, table.table_id, start, party_size=args.party_size, duration_hours=args.duration)
        print(f"Reserva creada: {format_public_id(r.reservation_id)}")
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

            elif choice == "2":
                number = int(input("Número de mesa: ").strip())
                capacity = int(input("Capacidad: ").strip())
                zone = input("Zona (terraza/interior/privado): ").strip()
                table = system.add_table(number, capacity, zone)
                print(f"Mesa creada: {format_public_id(table.table_id)}")

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
                print(f"Reserva creada: {format_public_id(reservation.reservation_id)}")

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

            elif choice == "8":
                reservation_id = input("ID de la reserva a cancelar: ").strip()
                reservation = system.cancel_reservation(reservation_id)
                print(f"Reserva cancelada: {format_public_id(reservation.reservation_id)}")

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

                updated = system.modify_reservation(reservation_id, table_id=table_id, start=new_start, party_size=new_party_size, duration_hours=new_duration)
                print(f"Reserva modificada: {format_public_id(updated.reservation_id)}")

            else:
                print("Opción inválida")

        except ReservationError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Entrada inválida: {e}")

    print("Saliendo de la interfaz interactiva. Se guarda la base de datos.")


if __name__ == "__main__":
    main()

