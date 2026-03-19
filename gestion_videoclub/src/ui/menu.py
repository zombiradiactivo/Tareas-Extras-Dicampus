import os
from datetime import date
from src.services.rental_service import RentalService
from src.database.db_handler import get_connection 

class MenuPrincipal:
    def __init__(self):
        self.rental_service = RentalService()

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_banner(self):
        print("="*40)
        print("🎬  SISTEMA DE GESTIÓN DE VIDEOCLUB  🎬")
        print("="*40)

    def listar_peliculas(self):
        print("\n--- 🎞️  CATÁLOGO DE PELÍCULAS ---")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, director, copias_disponibles FROM peliculas")
        rows = cursor.fetchall()
        
        print(f"{'ID':<4} | {'Título':<20} | {'Director':<15} | {'Stock'}")
        print("-" * 55)
        for row in rows:
            print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | {row[3]}")
        conn.close()
        input("\nPresione Enter para continuar...")

    def menu_alquiler(self):
        print("\n--- 📅  REGISTRAR NUEVO ALQUILER ---")
        try:
            id_cliente = int(input("ID del Cliente: "))
            id_pelicula = int(input("ID de la Película: "))
            
            exito = self.rental_service.registrar_alquiler(id_cliente, id_pelicula)
            if exito:
                print("✨ Operación completada con éxito.")
        except ValueError:
            print("❌ Error: Por favor, introduce números válidos.")
        input("\nPresione Enter para volver...")

    def menu_devolucion(self):
        print("\n--- 🔙  DEVOLUCIÓN DE PELÍCULA ---")
        try:
            id_alquiler = int(input("Introduce el ID del registro de Alquiler: "))
            multa = self.rental_service.procesar_devolucion(id_alquiler)
            
            if multa > 0:
                print(f"💰 Recuerda cobrar la multa de {multa:.2f}€")
        except ValueError:
            print("❌ Error: ID no válido.")
        input("\nPresione Enter para volver...")

    def ejecutar(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_banner()
            print("1. 🎞️  Ver Catálogo de Películas")
            print("2. 👤  Ver Clientes (Historial)")
            print("3. 🍿  Alquilar Película")
            print("4. 🔙  Devolver Película")
            print("5. 🚪  Salir")
            
            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":
                self.listar_peliculas()
            elif opcion == "2":
                print("No implementado todavia")
#                self.listar_clientes()
            elif opcion == "3":
                self.menu_alquiler()
            elif opcion == "4":
                self.menu_devolucion()
            elif opcion == "5":
                print("👋 ¡Gracias por usar el sistema! Saliendo...")
                break
            else:
                print("⚠️ Opción no válida. Intenta de nuevo.")
                import time
                time.sleep(1)