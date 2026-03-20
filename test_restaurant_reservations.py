import datetime
import pytest

from restaurant_reservations import ReservationSystem, ReservationError


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

    mesa_mas, count = system.most_reserved_table()
    assert mesa_mas.table_id in {t1.table_id, t2.table_id}
    assert count == 2 or count == 1

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
    system = ReservationSystem()
    c = system.add_customer("Carla", "222333444", "carla@example.com")
    t = system.add_table(30, 6, "terraza")
    start = datetime.datetime.now() + datetime.timedelta(days=2)
    r = system.create_reservation(c.customer_id, t.table_id, start, party_size=3)

    db_file = tmp_path / "test_reservations.db"
    system.save_to_db(str(db_file))

    new_sys = ReservationSystem()
    new_sys.load_from_db(str(db_file))

    assert len(new_sys.customers) == 1
    assert len(new_sys.tables) == 1
    assert len(new_sys.reservations) == 1
    loaded = next(iter(new_sys.reservations.values()))
    assert loaded.party_size == 3
    assert loaded.customer_id == c.customer_id

