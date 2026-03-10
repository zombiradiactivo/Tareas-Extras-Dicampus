import string
import secrets


def generar_contrasena(longitud, incluir_mayus, incluir_nums, incluir_simb, excluir_confusos):
    """
    Construye una contraseña aleatoria basada en un diccionario de parámetros.
    
    Args:
        params: Las configuraciones que se establecen en el menu_generar().
    Returns:
        str: La contraseña generada.
    """
    # El set base siempre son minúsculas para garantizar que no esté vacío
    caracteres = string.ascii_lowercase
    
    if incluir_mayus:
        caracteres += string.ascii_uppercase
    if incluir_nums:
        caracteres += string.digits
    if incluir_simb:
        caracteres += string.punctuation

    if excluir_confusos:
        confusos = "0OIl1"
        caracteres = "".join(c for c in caracteres if c not in confusos)
        print(f"  Caracteres disponibles tras filtrado: {len(caracteres)}")

    # Generación segura
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

