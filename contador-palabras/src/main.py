from utils.contador import calcular_estadisticas_lexicas, contar_parrafos, contar_oraciones, obtener_palabras_frecuentes
from utils.IO import capturar_texto_terminal, cargar_archivo, guardar_informe
import sys
import os


# --- INTERFAZ Y FLUJO ---

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