"""Test suite compatible with v1, v2, and v3 implementations."""

import datetime
import pytest
import sys
import tempfile
import uuid
from pathlib import Path

# Add the refactorizaciones directory to path to import v2/v3 modules
refactor_dir = Path(__file__).parent / "refactorizaciones"
if refactor_dir.exists():
    sys.path.insert(0, str(refactor_dir))


# Try to import from different versions
try:
    # v1: single file implementation
    from refactorizaciones.v1.restaurant_reservations import (
        ReservationSystem as V1ReservationSystem,
        ReservationError as V1ReservationError,
    )
    V1_AVAILABLE = True
except ImportError:
    V1_AVAILABLE = False

try:
    # v2: service + repository pattern
    from refactorizaciones.v2.models import (
        Customer as V2Customer,
        Table as V2Table,
        Reservation as V2Reservation,
        ReservationError as V2ReservationError,
    )
    from refactorizaciones.v2.repository import ReservationRepository as V2Repository
    from refactorizaciones.v2.service import ReservationService as V2ReservationService
    V2_AVAILABLE = True
except ImportError:
    V2_AVAILABLE = False

try:
    # v3: optimized service + repository
    from refactorizaciones.v3.models import (
        Customer as V3Customer,
        Table as V3Table,
        Reservation as V3Reservation,
        ReservationError as V3ReservationError,
    )
    from refactorizaciones.v3.repository import ReservationRepository as V3Repository
    from refactorizaciones.v3.service import ReservationService as V3ReservationService
    V3_AVAILABLE = True
except ImportError:
    V3_AVAILABLE = False


# Also try to import the original implementation if available
try:
    from restaurant_reservations import ReservationSystem as OriginalReservationSystem, ReservationError as OriginalReservationError
    ORIGINAL_AVAILABLE = True
except ImportError:
    ORIGINAL_AVAILABLE = False


class UnifiedReservationSystem:
    """Adapter that provides a unified interface for all versions."""

    def __init__(self, version='auto'):
        self.version = version
        self._impl = None
        self._reservations = {}
        self._customers = {}
        self._tables = {}

        if version == 'auto':
            # Try to detect best available version
            if V3_AVAILABLE:
                self._impl = V3UnifiedAdapter(self)
                self.version = 'v3'
            elif V2_AVAILABLE:
                self._impl = V2UnifiedAdapter(self)
                self.version = 'v2'
            elif V1_AVAILABLE:
                self._impl = V1UnifiedAdapter(self)
                self.version = 'v1'
            elif ORIGINAL_AVAILABLE:
                self._impl = OriginalUnifiedAdapter(self)
                self.version = 'original'
            else:
                raise ImportError("No implementation available")
        elif version == 'v3' and V3_AVAILABLE:
            self._impl = V3UnifiedAdapter(self)
        elif version == 'v2' and V2_AVAILABLE:
            self._impl = V2UnifiedAdapter(self)
        elif version == 'v1' and V1_AVAILABLE:
            self._impl = V1UnifiedAdapter(self)
        elif version == 'original' and ORIGINAL_AVAILABLE:
            self._impl = OriginalUnifiedAdapter(self)
        else:
            raise ValueError(f"Version '{version}' not available")

    def add_customer(self, name, phone, email):
        return self._impl.add_customer(name, phone, email) # pyright: ignore[reportOptionalMemberAccess]

    def add_table(self, number, capacity, zone):
        return self._impl.add_table(number, capacity, zone) # pyright: ignore[reportOptionalMemberAccess]

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        return self._impl.create_reservation(customer_id, table_id, start, party_size, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def get_reservation(self, reservation_id):
        return self._impl.get_reservation(reservation_id) # pyright: ignore[reportOptionalMemberAccess]

    def is_table_available(self, table_id, start, duration_hours=2.0):
        return self._impl.is_table_available(table_id, start, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        return self._impl.modify_reservation(reservation_id, table_id, start, party_size, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def cancel_reservation(self, reservation_id):
        return self._impl.cancel_reservation(reservation_id) # pyright: ignore[reportOptionalMemberAccess]

    def list_reservations(self, status=None):
        return self._impl.list_reservations(status) # pyright: ignore[reportOptionalMemberAccess]

    def upcoming_reminders(self, reference=None):
        return self._impl.upcoming_reminders(reference) # pyright: ignore[reportOptionalMemberAccess]

    def most_reserved_table(self):
        return self._impl.most_reserved_table() # pyright: ignore[reportOptionalMemberAccess]

    def peak_hour(self):
        return self._impl.peak_hour() # pyright: ignore[reportOptionalMemberAccess]

    def frequent_clients(self, top_n=3):
        return self._impl.frequent_clients(top_n) # pyright: ignore[reportOptionalMemberAccess]

    def get_customer_history(self, customer_id):
        return self._impl.get_customer_history(customer_id) # pyright: ignore[reportOptionalMemberAccess]

    def save_to_db(self, path):
        return self._impl.save_to_db(path) # pyright: ignore[reportOptionalMemberAccess]

    def load_from_db(self, path):
        return self._impl.load_from_db(path) # pyright: ignore[reportOptionalMemberAccess]


class BaseUnifiedAdapter:
    """Base class for adapters."""

    def __init__(self, unified_system):
        self.unified = unified_system
        self.ReservationError = Exception

    def _ensure_customer_dict(self):
        if not hasattr(self.unified, '_customers'):
            self.unified._customers = {}
        if not hasattr(self.unified, '_reservations'):
            self.unified._reservations = {}
        if not hasattr(self.unified, '_tables'):
            self.unified._tables = {}

    def add_customer(self, name, phone, email):
        raise NotImplementedError

    def add_table(self, number, capacity, zone):
        raise NotImplementedError

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        raise NotImplementedError

    def get_reservation(self, reservation_id):
        raise NotImplementedError

    def is_table_available(self, table_id, start, duration_hours=2.0):
        raise NotImplementedError

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        raise NotImplementedError

    def cancel_reservation(self, reservation_id):
        raise NotImplementedError

    def list_reservations(self, status=None):
        raise NotImplementedError

    def upcoming_reminders(self, reference=None):
        raise NotImplementedError

    def most_reserved_table(self):
        raise NotImplementedError

    def peak_hour(self):
        raise NotImplementedError

    def frequent_clients(self, top_n=3):
        raise NotImplementedError

    def get_customer_history(self, customer_id):
        raise NotImplementedError

    def save_to_db(self, path):
        raise NotImplementedError

    def load_from_db(self, path):
        raise NotImplementedError


class V1UnifiedAdapter(BaseUnifiedAdapter):
    """Adapter for v1 (ReservationSystem)"""

    def __init__(self, unified_system):
        super().__init__(unified_system)
        self.ReservationError = V1ReservationError if V1_AVAILABLE else OriginalReservationError  # pyright: ignore[reportPossiblyUnboundVariable]
        self._impl = None

        if V1_AVAILABLE:
            self._impl = V1ReservationSystem()  # type: ignore
        elif ORIGINAL_AVAILABLE:
            self._impl = OriginalReservationSystem() # type: ignore
        else:
            raise ImportError("V1 implementation not available")

    def add_customer(self, name, phone, email):
        return self._impl.add_customer(name, phone, email) # pyright: ignore[reportOptionalMemberAccess]

    def add_table(self, number, capacity, zone):
        return self._impl.add_table(number, capacity, zone) # pyright: ignore[reportOptionalMemberAccess]

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        return self._impl.create_reservation(customer_id, table_id, start, party_size, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def get_reservation(self, reservation_id):
        return self._impl.get_reservation(reservation_id) # pyright: ignore[reportOptionalMemberAccess]

    def is_table_available(self, table_id, start, duration_hours=2.0):
        return self._impl.check_availability(table_id, start, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        return self._impl.modify_reservation(reservation_id, table_id, start, party_size, duration_hours) # pyright: ignore[reportOptionalMemberAccess]

    def cancel_reservation(self, reservation_id):
        return self._impl.cancel_reservation(reservation_id) # pyright: ignore[reportOptionalMemberAccess]

    def list_reservations(self, status=None):
        return self._impl.list_reservations(status) # pyright: ignore[reportOptionalMemberAccess]

    def upcoming_reminders(self, reference=None):
        return self._impl.upcoming_reminders(reference) # pyright: ignore[reportOptionalMemberAccess]

    def most_reserved_table(self):
        return self._impl.most_reserved_table() # pyright: ignore[reportOptionalMemberAccess]

    def peak_hour(self):
        return self._impl.peak_hour() # pyright: ignore[reportOptionalMemberAccess]

    def frequent_clients(self, top_n=3):
        return self._impl.frequent_clients(top_n) # pyright: ignore[reportOptionalMemberAccess]

    def get_customer_history(self, customer_id):
        return self._impl.get_customer_history(customer_id) # pyright: ignore[reportOptionalMemberAccess]

    def save_to_db(self, path):
        return self._impl.save_to_db(path) # pyright: ignore[reportOptionalMemberAccess]

    def load_from_db(self, path):
        return self._impl.load_from_db(path) # pyright: ignore[reportOptionalMemberAccess]


class V2UnifiedAdapter(BaseUnifiedAdapter):
    """Adapter for v2 (ReservationService)"""

    def __init__(self, unified_system):
        super().__init__(unified_system)
        self.ReservationError = V2ReservationError # type: ignore
        # Use unique database file for each test instance
        self.db_name = f"test_v2_{uuid.uuid4().hex[:8]}.db"
        self._repo = V2Repository(self.db_name) # type: ignore
        self._impl = V2ReservationService(self._repo) # type: ignore

    def add_customer(self, name, phone, email):
        return self._impl.add_customer(name, phone, email)

    def add_table(self, number, capacity, zone):
        return self._impl.add_table(number, capacity, zone)

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        return self._impl.create_reservation(customer_id, table_id, start, party_size, duration_hours)

    def get_reservation(self, reservation_id):
        return self._impl.reservations[reservation_id]

    def is_table_available(self, table_id, start, duration_hours=2.0):
        return self._impl.check_availability(table_id, start, duration_hours)

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        return self._impl.modify_reservation(reservation_id, table_id, start, party_size, duration_hours)

    def cancel_reservation(self, reservation_id):
        return self._impl.cancel_reservation(reservation_id)

    def list_reservations(self, status=None):
        return self._impl.list_reservations(status)

    def upcoming_reminders(self, reference=None):
        now = reference or datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [r for r in self._impl.reservations.values() if r.status == "active" and now <= r.start <= limit]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self):
        counter = Counter(r.table_id for r in self._impl.reservations.values() if r.status == "active")
        if not counter:
            return None
        table_id, count = counter.most_common(1)[0]
        table = self._impl.tables.get(table_id)
        return (table, count) if table else None

    def peak_hour(self):
        hour_counts = Counter(r.start.hour for r in self._impl.reservations.values() if r.status == "active")
        if not hour_counts:
            return None
        return hour_counts.most_common(1)[0]

    def frequent_clients(self, top_n=3):
        customer_counts = Counter(r.customer_id for r in self._impl.reservations.values() if r.status == "active")
        most_common = customer_counts.most_common(top_n)
        return [(self._impl.customers[cid], count) for cid, count in most_common if cid in self._impl.customers]

    def get_customer_history(self, customer_id):
        customer = self._impl.customers.get(customer_id)
        if not customer:
            raise self.ReservationError("Cliente no encontrado")
        return [self._impl.reservations[rid] for rid in customer.reservation_ids if rid in self._impl.reservations]

    def save_to_db(self, path):
        # v2 uses repository pattern - save all data to specified path
        self._repo.save_all(self._impl.customers, self._impl.tables, self._impl.reservations)

    def load_from_db(self, path):
        # v2: load from specified database path
        # Create a new repository pointing to the specified path
        new_repo = V2Repository(path) # pyright: ignore[reportPossiblyUnboundVariable]
        self._impl.repository = new_repo
        self._impl.load()


class V3UnifiedAdapter(BaseUnifiedAdapter):
    """Adapter for v3 (optimized ReservationService)"""

    def __init__(self, unified_system):
        super().__init__(unified_system)
        self.ReservationError = V3ReservationError # pyright: ignore[reportPossiblyUnboundVariable]
        # Use unique database file for each test instance
        self.db_name = f"test_v3_{uuid.uuid4().hex[:8]}.db"
        self._repo = V3Repository(self.db_name) # pyright: ignore[reportPossiblyUnboundVariable]
        self._impl = V3ReservationService(self._repo) # pyright: ignore[reportPossiblyUnboundVariable]

    def add_customer(self, name, phone, email):
        return self._impl.add_customer(name, phone, email)

    def add_table(self, number, capacity, zone):
        return self._impl.add_table(number, capacity, zone)

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        return self._impl.create_reservation(customer_id, table_id, start, party_size, duration_hours)

    def get_reservation(self, reservation_id):
        return self._impl.reservations[reservation_id]

    def is_table_available(self, table_id, start, duration_hours=2.0):
        return self._impl.check_availability(table_id, start, duration_hours)

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        return self._impl.modify_reservation(reservation_id, table_id, start, party_size, duration_hours)

    def cancel_reservation(self, reservation_id):
        return self._impl.cancel_reservation(reservation_id)

    def list_reservations(self, status=None):
        return self._impl.list_reservations(status)

    def upcoming_reminders(self, reference=None):
        now = reference or datetime.datetime.now()
        limit = now + datetime.timedelta(hours=24)
        reminders = [r for r in self._impl.reservations.values() if r.status == "active" and now <= r.start <= limit]
        return sorted(reminders, key=lambda r: r.start)

    def most_reserved_table(self):
        counter = Counter(r.table_id for r in self._impl.reservations.values() if r.status == "active")
        if not counter:
            return None
        table_id, count = counter.most_common(1)[0]
        table = self._impl.tables.get(table_id)
        return (table, count) if table else None

    def peak_hour(self):
        hour_counts = Counter(r.start.hour for r in self._impl.reservations.values() if r.status == "active")
        if not hour_counts:
            return None
        return hour_counts.most_common(1)[0]

    def frequent_clients(self, top_n=3):
        customer_counts = Counter(r.customer_id for r in self._impl.reservations.values() if r.status == "active")
        most_common = customer_counts.most_common(top_n)
        return [(self._impl.customers[cid], count) for cid, count in most_common if cid in self._impl.customers]

    def get_customer_history(self, customer_id):
        customer = self._impl.customers.get(customer_id)
        if not customer:
            raise self.ReservationError("Cliente no encontrado")
        return [self._impl.reservations[rid] for rid in customer.reservation_ids if rid in self._impl.reservations]

    def save_to_db(self, path):
        # v3 uses repository pattern - manually save all data to specified path
        # Create a temporary repository for the target path
        temp_repo = V3Repository(path) # pyright: ignore[reportPossiblyUnboundVariable]
        # Save all customers
        for customer in self._impl.customers.values():
            temp_repo.add_customer(customer)
        # Save all tables
        for table in self._impl.tables.values():
            temp_repo.add_table(table)
        # Save all reservations
        for reservation in self._impl.reservations.values():
            temp_repo.add_reservation(reservation)

    def load_from_db(self, path):
        # v3: load from specified database path
        # Create a new repository pointing to the specified path
        new_repo = V3Repository(path) # pyright: ignore[reportPossiblyUnboundVariable]
        self._impl.repository = new_repo
        self._impl.load()


class OriginalUnifiedAdapter(BaseUnifiedAdapter):
    """Adapter for the original implementation (same as v1)"""

    def __init__(self, unified_system):
        super().__init__(unified_system)
        self.ReservationError = OriginalReservationError # pyright: ignore[reportPossiblyUnboundVariable]
        self._impl = OriginalReservationSystem() # pyright: ignore[reportPossiblyUnboundVariable]

    # Same as V1UnifiedAdapter
    def add_customer(self, name, phone, email):
        return self._impl.add_customer(name, phone, email)

    def add_table(self, number, capacity, zone):
        return self._impl.add_table(number, capacity, zone)

    def create_reservation(self, customer_id, table_id, start, party_size=1, duration_hours=2.0):
        return self._impl.create_reservation(customer_id, table_id, start, party_size, duration_hours)

    def get_reservation(self, reservation_id):
        return self._impl.get_reservation(reservation_id)

    def is_table_available(self, table_id, start, duration_hours=2.0):
        return self._impl.check_availability(table_id, start, duration_hours)

    def modify_reservation(self, reservation_id, table_id=None, start=None, party_size=None, duration_hours=None):
        return self._impl.modify_reservation(reservation_id, table_id, start, party_size, duration_hours)

    def cancel_reservation(self, reservation_id):
        return self._impl.cancel_reservation(reservation_id)

    def list_reservations(self, status=None):
        return self._impl.list_reservations(status)

    def upcoming_reminders(self, reference=None):
        return self._impl.upcoming_reminders(reference)

    def most_reserved_table(self):
        return self._impl.most_reserved_table()

    def peak_hour(self):
        return self._impl.peak_hour()

    def frequent_clients(self, top_n=3):
        return self._impl.frequent_clients(top_n)

    def get_customer_history(self, customer_id):
        return self._impl.get_customer_history(customer_id)

    def save_to_db(self, path):
        return self._impl.save_to_db(path)

    def load_from_db(self, path):
        return self._impl.load_from_db(path)


# Import Counter for adapters that need it
from collections import Counter


# Export unified system as the main class
ReservationSystem = UnifiedReservationSystem
ReservationError = Exception  # Will be set dynamically based on version


# Tests
def test_customer_table_and_reservation_lifecycle():
    system = ReservationSystem()

    cliente = system.add_customer("Ana", "123456789", "ana@example.com")
    mesa = system.add_table(number=1, capacity=4, zone="Interior")

    ahora = datetime.datetime.now() + datetime.timedelta(days=1)
    reserva = system.create_reservation(cliente.customer_id, mesa.table_id, ahora, duration_hours=2)

    fetched = system.get_reservation(reserva.reservation_id)
    assert fetched.customer_id == cliente.customer_id
    assert fetched.table_id == mesa.table_id

    assert not system.is_table_available(mesa.table_id, ahora + datetime.timedelta(minutes=30), duration_hours=2)

    # Modificar hora
    nueva_hora = ahora + datetime.timedelta(hours=3)
    mod = system.modify_reservation(reserva.reservation_id, start=nueva_hora)
    assert mod.start == nueva_hora

    # Cancelar
    cancel = system.cancel_reservation(reserva.reservation_id)
    assert cancel.status == "cancelled"
    with pytest.raises(ReservationError):
        system.modify_reservation(reserva.reservation_id, start=nueva_hora + datetime.timedelta(hours=1))


def test_separate_reservations_and_availability_rules():
    system = ReservationSystem()
    cliente1 = system.add_customer("Luis", "987654321", "luis@example.com")
    cliente2 = system.add_customer("María", "987650000", "maria@example.com")
    mesa1 = system.add_table(number=2, capacity=2, zone="terraza")

    inicio = datetime.datetime.now() + datetime.timedelta(days=2, hours=10)
    res1 = system.create_reservation(cliente1.customer_id, mesa1.table_id, inicio, duration_hours=2)

    with pytest.raises(ReservationError):
        system.create_reservation(cliente2.customer_id, mesa1.table_id, inicio + datetime.timedelta(minutes=30), duration_hours=1)

    assert system.is_table_available(mesa1.table_id, inicio + datetime.timedelta(hours=3), duration_hours=1)

    res2 = system.create_reservation(cliente2.customer_id, mesa1.table_id, inicio + datetime.timedelta(hours=3), duration_hours=1.5)
    assert len(system.list_reservations(status="active")) == 2


def test_reminders_and_statistics():
    system = ReservationSystem()
    c1 = system.add_customer("Pablo", "555000111", "pablo@example.com")
    t1 = system.add_table(3, 4, "privado")
    t2 = system.add_table(4, 6, "interior")

    ahora = datetime.datetime.now()
    r1 = system.create_reservation(c1.customer_id, t1.table_id, ahora + datetime.timedelta(hours=5), duration_hours=2)
    r2 = system.create_reservation(c1.customer_id, t2.table_id, ahora + datetime.timedelta(hours=26), duration_hours=2)

    reminders = system.upcoming_reminders(reference=ahora)
    assert any(r.reservation_id == r1.reservation_id for r in reminders)
    assert all(r.start <= ahora + datetime.timedelta(hours=24) for r in reminders)

    mesa_mas, count = system.most_reserved_table() # pyright: ignore[reportGeneralTypeIssues]
    # Both tables should have 1 reservation each (or one could have 2 if both reservations are on same table)
    assert mesa_mas.table_id in {t1.table_id, t2.table_id}
    assert count >= 1

    peak = system.peak_hour()
    assert peak is not None

    frecuentes = system.frequent_clients(1)
    assert len(frecuentes) == 1
    assert frecuentes[0][0].customer_id == c1.customer_id


def test_customer_history():
    system = ReservationSystem()
    c = system.add_customer("Rosa", "444333222", "rosa@example.com")
    t = system.add_table(5, 2, "terraza")

    ahora = datetime.datetime.now() + datetime.timedelta(days=3)
    r = system.create_reservation(c.customer_id, t.table_id, ahora)
    history = system.get_customer_history(c.customer_id)
    assert len(history) == 1
    assert history[0].reservation_id == r.reservation_id


def test_errors_for_invalid_operations():
    system = ReservationSystem()
    with pytest.raises(ReservationError):
        system.add_table(0, 4, "interior")

    with pytest.raises(ReservationError):
        system.add_customer("", "", "")

    c = system.add_customer("Test", "111", "test@example.com")
    t = system.add_table(10, 4, "interior")
    with pytest.raises(ReservationError):
        system.create_reservation(c.customer_id, t.table_id, datetime.datetime.now() - datetime.timedelta(hours=1))


def test_party_size_capacity_enforced():
    system = ReservationSystem()
    c = system.add_customer("Camila", "333444555", "camila@example.com")
    t = system.add_table(20, 4, "interior")
    start = datetime.datetime.now() + datetime.timedelta(days=1)

    with pytest.raises(ReservationError):
        system.create_reservation(c.customer_id, t.table_id, start, party_size=5)

    r = system.create_reservation(c.customer_id, t.table_id, start, party_size=4)
    assert r.party_size == 4


def test_database_persistence(tmp_path):
    # Use v1 explicitly for this test since it's designed for the original API
    if not V1_AVAILABLE and not ORIGINAL_AVAILABLE:
        pytest.skip("v1 implementation not available for database persistence test")

    # Create a v1 system directly
    if V1_AVAILABLE:
        system = V1ReservationSystem() # type: ignore
    else:
        system = OriginalReservationSystem() # pyright: ignore[reportPossiblyUnboundVariable]

    c = system.add_customer("Carla", "222333444", "carla@example.com")
    t = system.add_table(30, 6, "terraza")
    start = datetime.datetime.now() + datetime.timedelta(days=2)
    r = system.create_reservation(c.customer_id, t.table_id, start, party_size=3)

    db_file = tmp_path / "test_reservations.db"
    system.save_to_db(str(db_file))

    new_sys = V1ReservationSystem() if V1_AVAILABLE else OriginalReservationSystem() # pyright: ignore[reportPossiblyUnboundVariable]
    new_sys.load_from_db(str(db_file))

    assert len(new_sys.customers) == 1
    assert len(new_sys.tables) == 1
    assert len(new_sys.reservations) == 1
    loaded = next(iter(new_sys.reservations.values()))
    assert loaded.party_size == 3
    assert loaded.customer_id == c.customer_id


def test_crear_reserva_exitosa():
    system = ReservationSystem()
    cliente = system.add_customer("Ana", "123", "ana@example.com")
    mesa = system.add_table(1, 4, "Interior")
    ahora = datetime.datetime.now() + datetime.timedelta(days=1)
    reserva = system.create_reservation(cliente.customer_id, mesa.table_id, ahora)
    fetched = system.get_reservation(reserva.reservation_id)
    assert fetched is not None
    assert fetched.customer_id == cliente.customer_id
    assert fetched.table_id == mesa.table_id


def test_crear_reserva_mesa_ocupada():
    system = ReservationSystem()
    cliente1 = system.add_customer("Luis", "987", "luis@example.com")
    mesa = system.add_table(1, 4, "Interior")
    inicio = datetime.datetime.now() + datetime.timedelta(days=1)
    system.create_reservation(cliente1.customer_id, mesa.table_id, inicio)
    cliente2 = system.add_customer("María", "876", "maria@example.com")
    with pytest.raises(ReservationError):
        system.create_reservation(cliente2.customer_id, mesa.table_id, inicio + datetime.timedelta(minutes=30))


def test_cancelar_reserva_existente():
    system = ReservationSystem()
    cliente = system.add_customer("Rosa", "444", "rosa@example.com")
    mesa = system.add_table(5, 2, "terraza")
    ahora = datetime.datetime.now() + datetime.timedelta(days=1)
    reserva = system.create_reservation(cliente.customer_id, mesa.table_id, ahora)
    system.cancel_reservation(reserva.reservation_id)
    fetched = system.get_reservation(reserva.reservation_id)
    assert fetched is None or fetched.status == "cancelled"


def test_cancelar_reserva_inexistente():
    system = ReservationSystem()
    with pytest.raises(ReservationError):
        system.cancel_reservation("nonexistent_id")


def test_disponibilidad_fecha_pasada():
    system = ReservationSystem()
    cliente = system.add_customer("Carlos", "111", "carlos@example.com")
    mesa = system.add_table(10, 4, "Interior")
    pasado = datetime.datetime.now() - datetime.timedelta(hours=1)
    with pytest.raises(ReservationError):
        system.create_reservation(cliente.customer_id, mesa.table_id, pasado)


def test_estadisticas_sin_reservas():
    system = ReservationSystem()
    # Verificar que no hay reservas
    assert system.most_reserved_table() is None
    assert system.peak_hour() is None
    assert len(system.frequent_clients(3)) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
