import os

from gui.menu import menu_generar, ver_historial
from utils.utils import mostrar_bienvenida

# --- BUCLE PRINCIPAL ---

def main():
    """Bucle principal de la interfaz de usuario."""
    while True:
        mostrar_bienvenida()
        print("1. 🔑 Generar contraseña")
        print("2. 📜 Ver historial")
        print("3. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            menu_generar()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            print("\n¡Gracias por usar el Generador! Protege bien tus claves. 👋")
            break
        else:
            print("❌ Opción no válida.")
            input("Presiona Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()