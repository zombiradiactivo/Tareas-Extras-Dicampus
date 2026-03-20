from __future__ import annotations

import argparse
import datetime
import hashlib

from .repository import ReservationRepository
from .service import ReservationService
from .models import ReservationError


def format_public_id(expensive_id: str) -> str:
    return hashlib.sha256(expensive_id.encode()).hexdigest()[:10]


def main() -> None:
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

    repository = ReservationRepository(args.db)
    service = ReservationService(repository)

    try:
        if args.command == "add-customer":
            c = service.add_customer(args.name, args.phone, args.email)
            print(f"Cliente creado: {format_public_id(c.customer_id)}")

        elif args.command == "add-table":
            t = service.add_table(args.number, args.capacity, args.zone)
            print(f"Mesa creada: {format_public_id(t.table_id)}")

        elif args.command == "create-reservation":
            customer = service.get_customer_by_email(args.customer_email)
            table = next((t for t in service.tables.values() if t.number == args.table_number), None)
            if table is None:
                raise ReservationError("Mesa no encontrada")

            start = datetime.datetime.fromisoformat(args.start)
            r = service.create_reservation(customer.customer_id, table.table_id, start, party_size=args.party_size, duration_hours=args.duration)
            print(f"Reserva creada: {format_public_id(r.reservation_id)}")

        elif args.command == "list-reservations":
            reservations = service.list_reservations(status=args.status)
            for r in reservations:
                print(r)

        elif args.command is None:
            run_interactive_menu(service)

        else:
            parser.print_help()

    except ReservationError as exc:
        print(f"Error: {exc}")


def run_interactive_menu(service: ReservationService) -> None:
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
                customer = service.add_customer(name, phone, email)
                print(f"Cliente creado: {format_public_id(customer.customer_id)}")

            elif choice == "2":
                number = int(input("Número de mesa: ").strip())
                capacity = int(input("Capacidad: ").strip())
                zone = input("Zona (terraza/interior/privado): ").strip()
                table = service.add_table(number, capacity, zone)
                print(f"Mesa creada: {format_public_id(table.table_id)}")

            elif choice == "3":
                email = input("Email del cliente: ").strip()
                customer = service.get_customer_by_email(email)
                table_num = int(input("Número de mesa: ").strip())
                table = next((t for t in service.tables.values() if t.number == table_num), None)
                if table is None:
                    raise ReservationError("Mesa no encontrada")
                start = get_date("Inicio (YYYY-MM-DDTHH:MM): ")
                party = int(input("Tamaño del grupo: ").strip())
                duration = float(input("Duración (horas, default 2): ").strip() or 2.0)
                reservation = service.create_reservation(customer.customer_id, table.table_id, start, party_size=party, duration_hours=duration)
                print(f"Reserva creada: {format_public_id(reservation.reservation_id)}")

            elif choice == "4":
                status = input("Estado (active/cancelled/empty): ").strip() or None
                if status == "empty":
                    status = None
                for r in service.list_reservations(status=status):
                    print(r)

            elif choice == "5":
                table_num = int(input("Número de mesa: ").strip())
                table = next((t for t in service.tables.values() if t.number == table_num), None)
                if table is None:
                    raise ReservationError("Mesa no encontrada")
                start = get_date("Inicio (YYYY-MM-DDTHH:MM): ")
                duration = float(input("Duración (horas, default 2): ").strip() or 2.0)
                available = service.check_availability(table.table_id, start, duration)
                print("Disponible" if available else "No disponible")

            elif choice == "6":
                reminders = service.upcoming_reminders()
                if reminders:
                    for r in reminders:
                        print(r)
                else:
                    print("No hay reservas dentro de 24 horas")

            elif choice == "7":
                most_reserved = service.most_reserved_table()
                peak = service.peak_hour()
                frequent = service.frequent_clients(3)
                print(f"Mesa más reservada: {most_reserved}")
                print(f"Hora punta: {peak}")
                print("Clientes frecuentes:")
                for c, cnt in frequent:
                    print(f" {c.name} ({c.email}): {cnt}")

            elif choice == "8":
                reservation_id = input("ID de la reserva a cancelar: ").strip()
                r = service.cancel_reservation(reservation_id)
                print(f"Reserva cancelada: {format_public_id(r.reservation_id)}")

            elif choice == "9":
                reservation_id = input("ID de la reserva a modificar: ").strip()
                reservation = service.modify_reservation(reservation_id)
                print(f"Reserva modificada: {format_public_id(reservation.reservation_id)}")

            else:
                print("Opción inválida")

        except ReservationError as err:
            print(f"Error: {err}")
        except ValueError as err:
            print(f"Entrada inválida: {err}")

    print("Saliendo de la interfaz interactiva. Se guarda la base de datos.")


if __name__ == "__main__":
    main()
