from src_refactorizado.utils.calcular_estadisticas import calcular_estadisticas
from src_refactorizado.utils.mostrar_histograma import mostrar_histograma
from src_refactorizado.utils.obtener_entero import obtener_entero
from src_refactorizado.utils.menu import limpiar_pantalla
import random


def flujo_tirada():
    """
    Gestiona la configuración y ejecución de una nueva serie de dados.

    Pide al usuario el tipo de dado, cantidad y repeticiones, ejecuta
    la lógica de azar y muestra el resumen visual.

    Returns:
        dict or None: Datos de la tirada si tuvo éxito, None si el dado no es válido.
    """
    dados_validos = {"4": 4, "6": 6, "8": 8, "10": 10, "12": 12, "20": 20}
    print("\n--- Configuración de Tirada ---")
    eleccion = input("Elige caras (4, 6, 8, 10, 12, 20): ").strip()
    
    if eleccion in dados_validos:
        caras = dados_validos[eleccion]
        cant = obtener_entero("¿Cuántos dados? (1-10): ", 1, 10)
        reps = obtener_entero("¿Repeticiones? (1-20): ", 1, 20)
        
        historial = []
        limpiar_pantalla()
        print(f"🎲 Lanzando {cant}d{caras} x{reps} veces...\n")
        for i in range(1, reps + 1):
            t = [random.randint(1, caras) for _ in range(cant)]
            historial.append(t)
            print(f"#{i}: {t} (Suma: {sum(t)})")
        
        stats = calcular_estadisticas(historial)
        mostrar_histograma(historial, caras)
        return {"caras": caras, "cant": cant, "historial": historial, "stats": stats}
    else:
        print("❌ Tipo de dado no válido.")
        return None
