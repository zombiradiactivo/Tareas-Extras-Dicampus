import random
import os
from datetime import datetime

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    print("==========================================")
    print("🎲  BIENVENIDO AL SIMULADOR DE DADOS  🎲")
    print("      (D4, D6, D8, D10, D12, D20)       ")
    print("==========================================\n")

def guardar_en_archivo(caras, cantidad, historial_tiradas, estadisticas):
    if not historial_tiradas:
        print("⚠️ No hay datos en la sesión actual para guardar.")
        return

    if not os.path.exists('historial'):
        os.makedirs('historial')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"historial/tiradas_{timestamp}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"--- REPORTE DE TIRADAS ---\n")
        f.write(f"Configuración: {cantidad}d{caras}\n\n")
        for i, tirada in enumerate(historial_tiradas, 1):
            f.write(f"Tirada #{i}: {tirada} | Suma: {sum(tirada)}\n")
        f.write("\nESTADÍSTICAS:\n")
        for k, v in estadisticas.items():
            f.write(f"{k}: {v}\n")

    print(f"✅ Archivo guardado: {nombre_archivo}")

def mostrar_histograma(historial_tiradas, caras):
    todos_los_numeros = [v for t in historial_tiradas for v in t]
    frecuencias = {c: todos_los_numeros.count(c) for c in range(1, caras + 1)}
    max_f = max(frecuencias.values()) if frecuencias.values() else 0
    
    print("\n📊 HISTOGRAMA DE FRECUENCIAS:")
    for cara, cuenta in frecuencias.items():
        barra = "■" * (int((cuenta / max_f) * 20) if max_f > 0 else 0)
        print(f"Cara {cara:2}: {barra} ({cuenta})")

def calcular_estadisticas(historial_tiradas):
    sumas = [sum(t) for t in historial_tiradas]
    stats = {
        "Total": sum(sumas),
        "Media": round(sum(sumas) / len(sumas), 2),
        "Máximo": max(sumas),
        "Mínimo": min(sumas)
    }
    print("\n📈 ESTADÍSTICAS ACUMULADAS:")
    for k, v in stats.items():
        print(f" - {k}: {v}")
    return stats

def obtener_entero(msg, min_v, max_v):
    while True:
        entrada = input(msg).strip()
        if entrada.isdigit() and min_v <= int(entrada) <= max_v:
            return int(entrada)
        print(f"❌ Error: Introduce un número entre {min_v} y {max_v}.")

def flujo_tirada():
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

def main():
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

if __name__ == "__main__":
    main()