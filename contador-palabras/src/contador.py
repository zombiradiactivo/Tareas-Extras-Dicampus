from collections import Counter
from datetime import datetime
import sys
import re
import os

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
    
def contar_oraciones(texto):
    """
    Cuenta oraciones basándose en los delimitadores . ! y ?
    """
    if not texto.strip():
        return 0
    # Buscamos cualquier ocurrencia de los signos finales
    oraciones = re.findall(r'[^.!?]+[.!?]', texto)
    
    # Si el texto no termina en punto pero tiene contenido, contamos al menos 1
    return max(len(oraciones), 1 if texto.strip() else 0)

def contar_parrafos(texto):
    """
    Cuenta párrafos identificando bloques de texto separados por líneas vacías.
    """
    if not texto.strip():
        return 0
    # Dividimos por uno o más saltos de línea seguidos
    # \n{2,} detecta dos o más saltos de línea (una línea en blanco real)
    parrafos = re.split(r'\n\s*\n', texto.strip())
    return len(parrafos)

def obtener_palabras_frecuentes(texto, n=5):
    """
    Limpia el texto, filtra palabras vacías y devuelve las N más comunes.
    """
    # 1. Convertir a minúsculas y limpiar caracteres no alfanuméricos
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    
    # 2. Tokenizar (convertir en lista de palabras)
    palabras = texto_limpio.split()
    
    # 3. Lista de palabras vacías a ignorar
    stop_words = {'el', 'la', 'de', 'que', 'y', 'en', 'a', 'un', 'los', 'las', 'con', 'por'}
    
    # 4. Filtrar palabras
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 1]
    
    # 5. Contar y obtener el TOP N
    conteo = Counter(palabras_filtradas)
    return conteo.most_common(n)

def calcular_estadisticas_lexicas(texto):
    """
    Calcula métricas avanzadas: longitud media, palabras únicas y extremos.
    """
    # Limpieza estándar para conteo preciso
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    palabras = texto_limpio.split()
    
    if not palabras:
        return None

    # 1. Palabras únicas (Vocabulario)
    palabras_unicas = set(palabras)
    num_unicas = len(palabras_unicas)
    
    # 2. Porcentaje de palabras únicas (Riqueza léxica)
    porcentaje_unicas = (num_unicas / len(palabras)) * 100
    
    # 3. Longitud media (Suma de caracteres de todas las palabras / total palabras)
    longitud_media = sum(len(p) for p in palabras) / len(palabras)
    
    # 4. Palabra más larga y más corta
    # Usamos el texto original (sin lower) para que luzcan mejor en el informe
    palabras_originales = re.sub(r'[^\w\s]', '', texto).split()
    palabra_larga = max(palabras_originales, key=len)
    palabra_corta = min(palabras_originales, key=len)

    return {
        "unicas": num_unicas,
        "porcentaje": porcentaje_unicas,
        "media": longitud_media,
        "larga": palabra_larga,
        "corta": palabra_corta
    }

def cargar_archivo(ruta):
    """
    Lee el contenido de un archivo .txt con manejo de errores robusto.
    """
    # 1. Verificar si el archivo existe
    if not os.path.exists(ruta):
        print(f"❌ Error: El archivo en '{ruta}' no existe.")
        return None

    # 2. Verificar si es un archivo .txt
    if not ruta.lower().endswith('.txt'):
        print("❌ Error: El archivo debe tener extensión .txt.")
        return None

    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip()
            
            # 3. Verificar si el archivo está vacío
            if not contenido:
                print(f"⚠️ El archivo '{ruta}' está vacío.")
                return None
            
            return contenido

    except PermissionError:
        print("❌ Error: No tienes permisos para leer este archivo.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
    
    return None

def mostrar_informe(texto):
    # Cálculos previos
    palabras = len(texto.split())
    caracteres = len(texto)
    caracteres_sin_espacios_dobles = texto.replace('  ',' ')
    texto_sin_espacios = caracteres_sin_espacios_dobles.replace(' ','')

    # Nuevos cálculos
    oraciones = contar_oraciones(texto)
    parrafos = contar_parrafos(texto)
    
    # Nueva métrica: Top 5 palabras
    top_5 = obtener_palabras_frecuentes(texto, n=5)

    print("\n" + "="*30)
    print("📋 INFORME DE ANÁLISIS")
    print("="*30)
    print(f"🔹 Palabras:    {palabras}")
    print(f"🔹 Caracteres(con espacios):  {len(caracteres_sin_espacios_dobles)}")
    print(f"🔹 Caracteres(sin esapcios):  {len(texto_sin_espacios)}")    
    print(f"🔹 Oraciones:   {oraciones}")
    print(f"🔹 Párrafos:    {parrafos}")
    print("="*30 + "\n")
    print("🔝 TOP 5 PALABRAS MÁS FRECUENTES:")
    
    for i, (palabra, frec) in enumerate(top_5, 1):
        print(f"  {i}. '{palabra}': {frec} apariciones")
    
    print("="*40 + "\n")

def mostrar_informe_avanzado(texto):
    stats = calcular_estadisticas_lexicas(texto)
    if not stats:
        print("No hay suficiente texto para analizar.")
        return

    print("\n" + "╔" + "═"*45 + "╗")
    print("║" + "       📊 RESULTADOS DEL ANÁLISIS       ".center(45) + "║")
    print("╠" + "═"*45 + "╣")
    
    # Sección 1: Dimensiones
    print(f"║ 📝 Palabras totales: {len(texto.split()):<22} ║")
    print(f"║ 🔍 Palabras únicas:  {stats['unicas']:<22} ║")
    print(f"║ 📈 Riqueza léxica:   {stats['porcentaje']:>6.2f}%                ║")
    
    print("╠" + "─"*45 + "╢")
    
    # Sección 2: Estructura
    print(f"║ 📏 Longitud media:   {stats['media']:>6.2f} caracteres        ║")
    print(f"║ 🚀 Palabra más larga: {stats['larga'][:20]:<20} ║")
    print(f"║ 📍 Palabra más corta: {stats['corta'][:20]:<20} ║")
    
    print("╚" + "═"*45 + "╝\n")

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

def limpiar_pantalla():
    """Limpia la terminal dependiendo del sistema operativo."""
    # 'nt' es para Windows, 'posix' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    """Muestra un banner decorativo al inicio."""
    print("="*50)
    print("      📝 BIENVENIDO A TEXT-ANALYZER       ")
    print("="*50)
    print("  Tu herramienta de métricas y análisis léxico")
    print("="*50 + "\n")

def procesar_y_mostrar(texto, fuente):
    """Orquestador que llama a las funciones de análisis y muestra resultados."""
    limpiar_pantalla()
    
    # Realizar cálculos
    stats = calcular_estadisticas_lexicas(texto)
    top_5 = obtener_palabras_frecuentes(texto)
    oraciones = contar_oraciones(texto)
    parrafos = contar_parrafos(texto)
    
    # Mostrar resultados en pantalla
    mostrar_informe(texto)
    mostrar_informe_avanzado(texto)

    # Ofrecer guardar
    guardar_informe(texto, fuente, stats, top_5, oraciones, parrafos)
    
    input("\nPresiona ENTER para volver al menú principal...")

def menu_principal():
    while True:
        limpiar_pantalla()
        mostrar_bienvenida()
        
        print("1. ⌨️  Analizar texto manual")
        print("2. 📁  Analizar archivo (.txt)")
        print("3. ❌  Salir")
        print("-" * 50)
        
        opcion = input("\nSelecciona una opción (1-3): ")

        if opcion == "1":
            texto = capturar_texto_terminal() # Función de entrada manual
            fuente = "Entrada manual"
            if texto:
                procesar_y_mostrar(texto, fuente)
        
        elif opcion == "2":
            ruta = input("\nIntroduce la ruta del archivo (ej: textos/ejemplo.txt): ")
            texto = cargar_archivo(ruta) # Función de lectura de archivo
            fuente = f"Archivo: {ruta}"
            if texto:
                procesar_y_mostrar(texto, fuente)
        
        elif opcion == "3":
            print("\n¡Gracias por usar Text-Analyzer! Hasta pronto.\n")
            sys.exit() # Sale del programa limpiamente
        
        else:
            input("\n Opción no válida. Presiona ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()