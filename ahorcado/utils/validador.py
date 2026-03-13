import re

def limpiar_entrada(texto):
    """Elimina espacios extra y convierte a minúsculas."""
    return texto.strip().lower()

def validar_letra_ingresada(letra):
    """Verifica que sea exactamente una letra del alfabeto."""
    letra = limpiar_entrada(letra)
    # Solo permite letras de la 'a' a la 'z' (incluye ñ)
    if len(letra) == 1 and re.match(r'[a-zñ]', letra):
        return True, letra
    return False, "❌ Error: Ingresa solo una letra válida."

def validar_nueva_palabra(palabra):
    """Verifica que la palabra/frase solo contenga letras y espacios."""
    palabra = limpiar_entrada(palabra)
    if not palabra:
        return False, "❌ Error: La palabra no puede estar vacía."
    
    # Expresión regular: solo letras y espacios internos
    if re.fullmatch(r'[a-zñ\s]+', palabra):
        # Normalizar espacios múltiples a uno solo
        palabra_limpia = " ".join(palabra.split())
        return True, palabra_limpia
    
    return False, "❌ Error: Solo se permiten letras (sin números ni símbolos)."