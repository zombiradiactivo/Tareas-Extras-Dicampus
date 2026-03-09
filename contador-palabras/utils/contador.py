from collections import Counter
from config.config import STOP_WORDS as stop_words
import re

# --- LÓGICA DE ANÁLISIS (SRP) ---

def limpiar_texto(texto):
    """
    Elimina caracteres especiales y convierte el texto a minúsculas.
    
    Args:
        texto (str): El texto original.
    Returns:
        str: Texto procesado solo con caracteres alfanuméricos.
    """
    return re.sub(r'[^\w\s]', '', texto.lower())

def contar_oraciones(texto):
    """Cuenta oraciones basándose en los delimitadores . ! y ?."""
    if not texto.strip(): return 0
    oraciones = re.findall(r'[^.!?]+[.!?]', texto)
    return max(len(oraciones), 1 if texto.strip() else 0)

def contar_parrafos(texto):
    """Cuenta párrafos identificando bloques separados por líneas vacías."""
    if not texto.strip(): return 0
    return len(re.split(r'\n\s*\n', texto.strip()))

def obtener_palabras_frecuentes(texto, n=5):
    """
    Limpia el texto, filtra palabras vacías y devuelve las N más comunes.
    """
    # 1. Convertir a minúsculas y limpiar caracteres no alfanuméricos
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    
    # 2. Tokenizar (convertir en lista de palabras)
    palabras = texto_limpio.split()
        
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
