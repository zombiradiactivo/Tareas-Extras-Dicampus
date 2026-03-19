import random
import os
from datetime import datetime

def guardar_en_archivo(caras, cantidad, historial_tiradas, estadisticas):
    """
    Crea la carpeta historial/ y guarda los datos en un archivo .txt con timestamp.
    """
    if not os.path.exists('historial'):
        os.makedirs('historial')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"historial/tiradas_{timestamp}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"--- REPORTE DE TIRADAS ---\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Configuración: {cantidad}d{caras}\n\n")
        
        f.write("DETALLE DE LANZAMIENTOS:\n")
        for i, tirada in enumerate(historial_tiradas, 1):
            f.write(f"Tirada #{i}: {tirada} | Suma: {sum(tirada)}\n")
        
        f.write("\nESTADÍSTICAS:\n")
        for clave, valor in estadisticas.items():
            f.write(f"{clave}: {valor}\n")

    print(f"\n✅ Historial guardado con éxito en: {nombre_archivo}")

def mostrar_histograma(historial_tiradas, caras):
    todos_los_numeros = [valor for tirada in historial_tiradas for valor in tirada]
    frecuencias = {cara: todos_los_numeros.count(cara) for cara in range(1, caras + 1)}
    max_frecuencia = max(frecuencias.values()) if frecuencias.values() else 0
    ancho_maximo = 20

    print("\n📊 DISTRIBUCIÓN DE RESULTADOS")
    for cara, cuenta in frecuencias.items():
        longitud_barra = int((cuenta / max_frecuencia) * ancho_maximo) if max_frecuencia > 0 else 0
        print(f"Cara {cara:2}: {'■' * longitud_barra} ({cuenta})")

def calcular_estadisticas(historial_tiradas):
    sumas = [sum(t) for t in historial_tiradas]
    stats = {
        "Suma Total": sum(sumas),
        "Media x Tirada": round(sum(sumas) / len(sumas), 2),
        "Valor Máximo": max(sumas),
        "Valor Mínimo": min(sumas)
    }
    
    print("\n" + "="*30)
    print("📈 RESUMEN DE LA SERIE")
    for k, v in stats.items():
        print(f"🔹 {k}: {v}")
    print("="*30)
    return stats

def lanzar_dados(caras, cantidad, repeticiones):
    historial_sesion = []
    for i in range(1, repeticiones + 1):
        tirada_actual = [random.randint(1, caras) for _ in range(cantidad)]
        historial_sesion.append(tirada_actual)
        print(f"Tirada #{i}: {tirada_actual} | Suma: {sum(tirada_actual)}")

    stats = calcular_estadisticas(historial_sesion)
    mostrar_histograma(historial_sesion, caras)

    confirmacion = input("\n¿Deseas guardar este historial en un archivo? (s/n): ").lower()
    if confirmacion == 's':
        guardar_en_archivo(caras, cantidad, historial_sesion, stats)

def obtener_entero_validado(mensaje, min_val, max_val):
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit() and min_val <= int(entrada) <= max_val:
            return int(entrada)
        print(f"❌ Error: Introduce un número entre {min_val} y {max_val}.")

def seleccionar_dado():
    dados_validos = {"4": 4, "6": 6, "8": 8, "10": 10, "12": 12, "20": 20}
    while True:
        print("\n--- Menú de Dados ---")
        eleccion = input("Elige caras (4, 6, 8, 10, 12, 20) o 'salir': ").strip()
        if eleccion.lower() == 'salir': return None
        if eleccion in dados_validos: return dados_validos[eleccion]
        print("❌ Error: Dado no válido.")

if __name__ == "__main__":
    caras = seleccionar_dado()
    if caras:
        cantidad = obtener_entero_validado("¿Cuántos dados? (1-10): ", 1, 10)
        repeticiones = obtener_entero_validado("¿Repeticiones? (1-20): ", 1, 20)
        lanzar_dados(caras, cantidad, repeticiones)