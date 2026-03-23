from __future__ import annotations

import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

from .models import Customer, Reservation, ReservationError, Table
from .repository import ReservationRepository

MAX_CUSTOMER_NAME = 100
MAX_CUSTOMER_PHONE = 20
MAX_CUSTOMER_EMAIL = 100
VALID_ZONES = {"terraza", "interior", "privado"}
DEFAULT_RESERVATION_DURATION_HOURS = 2.0


class ReservationService:
    def __init__(self, repository: ReservationRepository):
        self.repository = repository
        self.customers: Dict[str, Customer] = {}
        self.customers_by_email: Dict[str, Customer] = {}
        self.tables: Dict[str, Table] = {}
        self.tables_by_number: Dict[int, Table] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.reservations_by_table: Dict[str, List[Reservation]] = defaultdict(list)
        self.load()

    def load(self):
        self.customers, self.tables, self.reservations = self.repository.load_all()

        self.customers_by_email = {c.email: c for c in self.customers.values()}
        self.tables_by_number = {t.number: t for t in self.tables.values()}

        self.reservations_by_table.clear()
        for res in self.reservations.values():
            self.reservations_by_table[res.table_id].append(res)

        for reservations in self.reservations_by_table.values():
            reservations.sort(key=lambda r: r.start)

        for customer in self.customers.values():
            customer.reservation_ids = [
                r.reservation_id
                for r in self.reservations.values()
                if r.customer_id == customer.customer_id
            ]

    def _index_reservation(self, reservation: Reservation):
        self.reservations[reservation.reservation_id] = reservation
        self.reservations_by_table[reservation.table_id].append(reservation)
        self.reservations_by_table[reservation.table_id].sort(key=lambda r: r.start)
        self.customers[reservation.customer_id].reservation_ids.append(reservation.reservation_id)

    def _reindex_reservation(self, reservation: Reservation, old_table_id: str):
        self.reservations[reservation.reservation_id] = reservation
        if old_table_id != reservation.table_id:
            self.reservations_by_table[old_table_id] = [r for r in self.reservations_by_table[old_table_id] if r.reservation_id != reservation.reservation_id]
            self.reservations_by_table[reservation.table_id].append(reservation)
        self.reservations_by_table[reservation.table_id].sort(key=lambda r: r.start)

    def _check_reservation_time_limits(self, start: datetime.datetime):
        if start < datetime.datetime.now():
            raise ReservationError("La fecha y hora debe ser en el futuro")

    def _check_party_size(self, party_size: int, table: Table):
        if party_size <= 0 or party_size > table.capacity:
            raise ReservationError("Tamaño inválido para la mesa")

    @staticmethod
    def _is_overlapping(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime) -> bool:
        return start1 < end2 and start2 < end1

    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        normalized = email.strip().lower()
        name = name.strip()
        phone = phone.strip()

        if not (name and phone and normalized):
            raise ReservationError("Nombre, teléfono y email son obligatorios")

        if len(name) > MAX_CUSTOMER_NAME or len(phone) > MAX_CUSTOMER_PHONE or len(normalized) > MAX_CUSTOMER_EMAIL:
            raise ReservationError("Campos exceden longitud máxima aceptada")

        if normalized in self.customers_by_email:
            raise ReservationError("Email ya registrado")

        customer = Customer(name=name, phone=phone, email=normalized)
        self.customers[customer.customer_id] = customer
        self.customers_by_email[normalized] = customer
        self.repository.add_customer(customer)
        return customer

    def get_customer_by_email(self, email: str) -> Customer:
        normalized = email.strip().lower()

        if normalized in self.customers_by_email:
            return self.customers_by_email[normalized]

        persistent = self.repository.get_customer_by_email(normalized)
        if persistent:
            self.customers[persistent.customer_id] = persistent
            self.customers_by_email[normalized] = persistent
            return persistent

        raise ReservationError("Cliente no encontrado")

    def add_table(self, number: int, capacity: int, zone: str) -> Table:
        if number <= 0 or capacity <= 0:
            raise ReservationError("Número y capacidad de mesa deben ser mayores que 0")

        zone_clean = zone.strip().lower()
        if zone_clean not in VALID_ZONES:
            raise ReservationError("Zona debe ser terraza, interior o privado")

        if number in self.tables_by_number:
            raise ReservationError("Número de mesa ya existe")

        table = Table(number=number, capacity=capacity, zone=zone_clean)
        self.tables[table.table_id] = table
        self.tables_by_number[number] = table
        self.repository.add_table(table)
        return table

    def check_availability(
        self,
        table_id: str,
        start: datetime.datetime,
        duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS,
        exclude_reservation_id: Optional[str] = None,
    ) -> bool:
        if duration_hours <= 0:
            raise ReservationError("Duración inválida")

        table = self.tables.get(table_id)
        if not table:
            raise ReservationError("Mesa no encontrada")

        end = start + datetime.timedelta(hours=duration_hours)
        schedule = self.reservations_by_table.get(table_id, [])

        for existing in schedule:
            if existing.status != "active" or (exclude_reservation_id and existing.reservation_id == exclude_reservation_id):
                continue

            if self._is_overlapping(existing.start, existing.end, start, end):
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
        customer = self.customers.get(customer_id)
        if not customer:
            raise ReservationError("Cliente no registrado")

        table = self.tables.get(table_id)
        if not table:
            raise ReservationError("Mesa no encontrada")

        self._check_party_size(party_size, table)
        self._check_reservation_time_limits(start)

        if not self.check_availability(table_id, start, duration_hours):
            raise ReservationError("La mesa no está disponible en ese horario")

        reservation = Reservation(
            customer_id=customer_id,
            table_id=table_id,
            start=start,
            end=start + datetime.timedelta(hours=duration_hours),
            party_size=party_size,
        )

        self._index_reservation(reservation)
        self.repository.add_reservation(reservation)
        return reservation

    def cancel_reservation(self, reservation_id: str) -> Reservation:
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            raise ReservationError("Reserva no encontrada")

        if reservation.status == "cancelled":
            raise ReservationError("Reserva ya cancelada")

        reservation.status = "cancelled"
        self.repository.update_reservation(reservation)
        return reservation

    def modify_reservation(
        self,
        reservation_id: str,
        table_id: Optional[str] = None,
        start: Optional[datetime.datetime] = None,
        party_size: Optional[int] = None,
        duration_hours: Optional[float] = None,
    ) -> Reservation:
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            raise ReservationError("Reserva no encontrada")

        if reservation.status != "active":
            raise ReservationError("Solo se pueden modificar reservas activas")

        old_table_id = reservation.table_id

        new_table_id = table_id or reservation.table_id
        new_start = start or reservation.start
        new_party_size = party_size if party_size is not None else reservation.party_size
        new_duration = (
            duration_hours
            if duration_hours is not None
            else (reservation.end - reservation.start).total_seconds() / 3600
        )

        table = self.tables.get(new_table_id)
        if not table:
            raise ReservationError("Mesa no encontrada")

        self._check_party_size(new_party_size, table)
        self._check_reservation_time_limits(new_start)

        if not self.check_availability(new_table_id, new_start, new_duration, exclude_reservation_id=reservation_id):
            raise ReservationError("Horario no disponible")

        reservation.table_id = new_table_id
        reservation.start = new_start
        reservation.end = new_start + datetime.timedelta(hours=new_duration)
        reservation.party_size = new_party_size

        self._reindex_reservation(reservation, old_table_id)
        self.repository.update_reservation(reservation)
        return reservation

    def list_reservations(self, status: Optional[str] = None) -> List[Reservation]:
        if status is None:
            return list(self.reservations.values())

        return [r for r in self.reservations.values() if r.status == status]

    def upcoming_reminders(self) -> List[Reservation]:
        now = datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [
            r for r in self.reservations.values() if r.status == "active" and now <= r.start <= limit
        ]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self) -> Optional[Tuple[Table, int]]:
        counter = Counter(r.table_id for r in self.reservations.values() if r.status == "active")
        if not counter:
            return None

        table_id, count = counter.most_common(1)[0]
        table = self.tables.get(table_id)
        if not table:
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
