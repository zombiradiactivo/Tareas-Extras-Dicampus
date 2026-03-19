from datetime import datetime
import os

def guardar_en_archivo(caras, cantidad, historial_tiradas, estadisticas):
    """
    Registra los resultados de la sesión actual en un archivo de texto.

    Crea un directorio 'historial' si no existe y genera un archivo único
    nombrado con la fecha y hora actual (ISO 8601 simplificado).

    Args:
        caras (int): Número de caras del dado utilizado.
        cantidad (int): Cuántos dados se lanzaron por tirada.
        historial_tiradas (list): Lista de listas con los resultados numéricos.
        estadisticas (dict): Diccionario con los cálculos de la serie.
    """
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

