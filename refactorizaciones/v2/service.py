from __future__ import annotations

import datetime
from collections import Counter
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
        self.tables: Dict[str, Table] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.load()

    def load(self):
        self.customers, self.tables, self.reservations = self.repository.load_all()
        for customer in self.customers.values():
            customer.reservation_ids = [
                r.reservation_id
                for r in self.reservations.values()
                if r.customer_id == customer.customer_id
            ]

    def save(self):
        self.repository.save_all(self.customers, self.tables, self.reservations)

    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        name = name.strip()
        phone = phone.strip()
        email = email.strip()

        if not (name and phone and email):
            raise ReservationError("Nombre, teléfono y email son obligatorios")

        if len(name) > MAX_CUSTOMER_NAME or len(phone) > MAX_CUSTOMER_PHONE or len(email) > MAX_CUSTOMER_EMAIL:
            raise ReservationError("Campos exceden longitud máxima aceptada")

        if any(c.email == email for c in self.customers.values()):
            raise ReservationError("Email ya registrado")

        customer = Customer(name=name, phone=phone, email=email)
        self.customers[customer.customer_id] = customer
        self.save()
        return customer

    def get_customer_by_email(self, email: str) -> Customer:
        normalized = email.strip()

        for customer in self.customers.values():
            if customer.email == normalized:
                return customer

        persistent = self.repository.get_customer_by_email(normalized)
        if persistent:
            self.customers[persistent.customer_id] = persistent
            return persistent

        raise ReservationError("Cliente no encontrado")

    def add_table(self, number: int, capacity: int, zone: str) -> Table:
        if number <= 0 or capacity <= 0:
            raise ReservationError("Número y capacidad de mesa deben ser mayores que 0")

        zone_clean = zone.strip().lower()
        if zone_clean not in VALID_ZONES:
            raise ReservationError("Zona debe ser terraza, interior o privado")

        if any(t.number == number for t in self.tables.values()):
            raise ReservationError("Número de mesa ya existe")

        table = Table(number=number, capacity=capacity, zone=zone_clean)
        self.tables[table.table_id] = table
        self.save()
        return table

    @staticmethod
    def _is_overlapping(start1: datetime.datetime, end1: datetime.datetime, start2: datetime.datetime, end2: datetime.datetime) -> bool:
        return start1 < end2 and start2 < end1

    def check_availability(self, table_id: str, start: datetime.datetime, duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS, exclude_reservation_id: Optional[str] = None) -> bool:
        if duration_hours <= 0:
            raise ReservationError("Duración inválida")

        if table_id not in self.tables:
            raise ReservationError("Mesa no encontrada")

        end = start + datetime.timedelta(hours=duration_hours)

        for reservation in self.reservations.values():
            if reservation.table_id != table_id or reservation.status != "active":
                continue

            if exclude_reservation_id and reservation.reservation_id == exclude_reservation_id:
                continue

            if self._is_overlapping(reservation.start, reservation.end, start, end):
                return False

        return True

    def create_reservation(self, customer_id: str, table_id: str, start: datetime.datetime, party_size: int = 1, duration_hours: float = DEFAULT_RESERVATION_DURATION_HOURS) -> Reservation:
        if customer_id not in self.customers:
            raise ReservationError("Cliente no registrado")

        if table_id not in self.tables:
            raise ReservationError("Mesa no encontrada")

        table = self.tables[table_id]

        if party_size <= 0 or party_size > table.capacity:
            raise ReservationError("Tamaño inválido para la mesa")

        if start < datetime.datetime.now():
            raise ReservationError("La fecha y hora debe ser en el futuro")

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
        self.save()
        return reservation

    # Additional methods for cancel/modify/list as needed
    def cancel_reservation(self, reservation_id: str) -> Reservation:
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            raise ReservationError("Reserva no encontrada")

        if reservation.status == "cancelled":
            raise ReservationError("Reserva ya cancelada")

        reservation.status = "cancelled"
        self.save()
        return reservation

    def modify_reservation(self, reservation_id: str, table_id: Optional[str] = None, start: Optional[datetime.datetime] = None, party_size: Optional[int] = None, duration_hours: Optional[float] = None) -> Reservation:
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            raise ReservationError("Reserva no encontrada")

        if reservation.status != "active":
            raise ReservationError("Solo se pueden modificar reservas activas")

        new_table_id = table_id if table_id is not None else reservation.table_id
        new_start = start if start is not None else reservation.start
        new_party_size = party_size if party_size is not None else reservation.party_size
        new_duration = duration_hours if duration_hours is not None else (reservation.end - reservation.start).total_seconds()/3600

        if new_table_id not in self.tables:
            raise ReservationError("Mesa no encontrada")

        table = self.tables[new_table_id]

        if new_party_size <= 0 or new_party_size > table.capacity:
            raise ReservationError("Tamaño inválido para la mesa")

        if new_start < datetime.datetime.now():
            raise ReservationError("La fecha y hora debe ser en el futuro")

        if not self.check_availability(new_table_id, new_start, new_duration, exclude_reservation_id=reservation_id):
            raise ReservationError("Horario no disponible")

        reservation.table_id = new_table_id
        reservation.start = new_start
        reservation.end = new_start + datetime.timedelta(hours=new_duration)
        reservation.party_size = new_party_size

        self.save()
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
