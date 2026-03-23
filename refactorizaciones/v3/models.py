from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field
from typing import List


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
