import string


def evaluar_fortaleza(password):
    """
    Analiza la robustez de una cadena basándose en entropía y diversidad.
    
    Args:
        password (str): La contraseña a evaluar.
    Returns:
        str: Etiqueta de fortaleza (Débil, Media, Fuerte, Muy Fuerte).
    """
    puntos = 0
    longitud = len(password)
    
    # 1. Evaluación por Longitud
    if longitud >= 12: puntos += 2
    elif longitud >= 8: puntos += 1
    
    # 2. Evaluación por Diversidad (Presencia de tipos)
    tiene_mayus = any(c.isupper() for c in password)
    tiene_minus = any(c.islower() for c in password)
    tiene_num = any(c.isdigit() for c in password)
    tiene_simbolo = any(c in string.punctuation for c in password)
    
    if tiene_mayus: puntos += 1
    if tiene_minus: puntos += 1
    if tiene_num: puntos += 1
    if tiene_simbolo: puntos += 1
    
    # Determinamos la categoría según los puntos (Máximo 6 puntos)
    if puntos >= 6:
        return "Muy Fuerte 🛡️", "VERDE"
    elif puntos >= 4:
        return "Fuerte 💪", "AZUL"
    elif puntos >= 3:
        return "Media ⚠️", "AMARILLO"
    else:
        return "Débil ❌", "ROJO"
