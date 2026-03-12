from utils.utils import limpiar_pantalla


def mostrar_menu(opciones):
    print("\n--- SELECCIONA TU MOVIMIENTO ---")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    print("---------------------------------")


def mostrar_bienvenida():
    limpiar_pantalla()
    print("="*50)
    print("      SÚPER PIEDRA-PAPEL-TIJERAS: NIVEL 2      ")
    print("="*50)
    input("\nPresiona ENTER para configurar tu partida...")
