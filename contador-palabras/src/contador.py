import sys
import re
from collections import Counter
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


if __name__ == "__main__":
    texto = capturar_texto_terminal()
    if texto:
        mostrar_informe(texto)
        mostrar_informe_avanzado(texto)
