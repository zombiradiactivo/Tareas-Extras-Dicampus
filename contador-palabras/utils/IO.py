from datetime import datetime
import os

# --- ENTRADA Y SALIDA (I/O) ---

def cargar_archivo(ruta):
    """Lee un archivo .txt con manejo de excepciones."""
    if not os.path.exists(ruta):
        print(f"❌ Error: No existe el archivo '{ruta}'.")
        return None
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            return contenido if contenido else (print("⚠️ Archivo vacío."), None)[1]
    except Exception as e:
        print(f"❌ Error al leer: {e}")
        return None

def capturar_texto_terminal():
    """
    Pide al usuario introducir texto multilínea. 
    Se termina la captura dejando una línea en blanco (pulsando Enter dos veces).
    """
    print("\n--- Modo: Entrada Manual ---")
    print("Escribe tu texto. Para terminar, escribe la palabra 'FIN' en una línea nueva.")    

    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":  # Ahora termina con la palabra FIN
            break
        lineas.append(linea)
    
    # Unimos las líneas con saltos de línea
    texto_final = "\n".join(lineas).strip()

    # Manejar el caso en que el usuario no introduzca nada
    if not texto_final:
        print("\n Error: No has introducido ningún texto.")
        return None

    # Mostrar el texto de vuelta para confirmación
    print("\n--- Texto Recibido ---")
    print(texto_final)
    print("----------------------")
    
    confirmar = input("\n¿Es correcto este texto? (s/n): ").lower()
    if confirmar == 's':
        return texto_final
    else:
        print("Operación cancelada por el usuario.")
        return None


def guardar_informe(texto, fuente, stats, top_5, oraciones, parrafos):
    """
    Genera un archivo .txt con el informe completo y lo guarda en docs/.
    """
    confirmacion = input("¿Deseas guardar el informe en un archivo? (s/n): ").lower()
    
    if confirmacion != 's':
        print("Informe no guardado.")
        return

    # Crear el nombre del archivo con la fecha actual para evitar sobreescrituras
    ahora = datetime.now()
    fecha_str = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    ruta_destino = f"docs/informe_{fecha_str}.txt"
    caracteres_sin_espacios_dobles = texto.replace('  ',' ')
    texto_sin_espacios = caracteres_sin_espacios_dobles.replace(' ','')

    try:
        with open(ruta_destino, 'w', encoding='utf-8') as f:
            f.write("==========================================\n")
            f.write("      INFORME DE ANÁLISIS DE TEXTO        \n")
            f.write("==========================================\n\n")
            
            f.write(f"📅 Fecha y hora: {ahora.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"📂 Fuente: {fuente}\n")
            f.write("-" * 42 + "\n\n")
            
            # Estadísticas Básicas
            f.write(f"📝 Palabras totales: {len(texto.split())}\n")
            f.write(f"📜 Oraciones:        {oraciones}\n")
            f.write(f"📂 Párrafos:         {parrafos}\n")
            f.write(f"🔹 Caracteres(con espacios):  {len(caracteres_sin_espacios_dobles)}")
            f.write(f"🔹 Caracteres(sin esapcios):  {len(texto_sin_espacios)}")  
            f.write(f"🔍 Palabras únicas:  {stats['unicas']}\n")
            f.write(f"📈 Riqueza léxica:   {stats['porcentaje']:.2f}%\n")
            f.write(f"📏 Longitud media:   {stats['media']:.2f} caracteres\n\n")
            
            # Palabras extremas
            f.write(f"🚀 Palabra más larga: {stats['larga']}\n")
            f.write(f"📍 Palabra más corta: {stats['corta']}\n\n")
            
            # Top 5
            f.write("🔝 TOP 5 PALABRAS MÁS FRECUENTES:\n")
            for i, (palabra, frec) in enumerate(top_5, 1):
                f.write(f"   {i}. '{palabra}': {frec} apariciones\n")
            
            f.write("\n" + "="*42 + "\n")
            f.write("Generado por: Contador-Palabras Pro\n")

        print(f"\n✅ Informe guardado con éxito en: {ruta_destino}")
        
    except Exception as e:
        print(f"❌ No se pudo guardar el archivo: {e}")
