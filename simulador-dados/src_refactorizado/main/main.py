from src_refactorizado.utils.calcular_estadisticas import calcular_estadisticas
from src_refactorizado.utils.flujo_tirada import flujo_tirada
from src_refactorizado.utils.menu import limpiar_pantalla, mostrar_bienvenida
from src_refactorizado.utils.guardar_en_archivo import guardar_en_archivo


def main():
    """
    Punto de entrada principal del simulador.
    
    Controla el bucle del menú principal y la navegación entre las
    diferentes opciones de la aplicación.
    """
    sesion_actual = None
    
    while True:
        limpiar_pantalla()
        mostrar_bienvenida()
        print("1. Nueva Tirada")
        print("2. Ver Historial de Sesión (Última serie)")
        print("3. Guardar Historial en Archivo")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            sesion_actual = flujo_tirada()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == "2":
            if sesion_actual:
                limpiar_pantalla()
                print("📋 HISTORIAL DE LA ÚLTIMA SERIE:")
                for i, t in enumerate(sesion_actual['historial'], 1):
                    print(f"Tirada {i}: {t}")
                calcular_estadisticas(sesion_actual['historial'])
            else:
                print("⚠️ No hay tiradas recientes.")
            input("\nPresiona Enter para volver al menú...")
        elif opcion == "3":
            if sesion_actual:
                guardar_en_archivo(sesion_actual['caras'], sesion_actual['cant'], 
                                   sesion_actual['historial'], sesion_actual['stats'])
            else:
                print("⚠️ No hay nada que guardar.")
            input("\nPresiona Enter para volver al menú...")
        elif opcion == "4":
            print("¡Gracias por usar el simulador! 👋")
            break
        else:
            print("❌ Opción no válida.")
            input("\nPresiona Enter para reintentar...")
