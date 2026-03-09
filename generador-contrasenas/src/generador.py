import string
import secrets

def generar_contrasena_basica(longitud=12):
    """
    Genera una contraseña segura combinando todos los tipos de caracteres.
    """
    # Definimos los grupos de caracteres
    letras_min = string.ascii_lowercase
    letras_may = string.ascii_uppercase
    numeros = string.digits
    simbolos = string.punctuation
    
    # Combinamos todos los caracteres posibles
    todos_los_caracteres = letras_min + letras_may + numeros + simbolos
    
    # Generamos la contraseña asegurando aleatoriedad criptográfica
    # secrets.choice es ideal para este propósito
    contrasena = ''.join(secrets.choice(todos_los_caracteres) for _ in range(longitud))
    
    return contrasena

# --- Bloque de ejecución ---
if __name__ == "__main__":
    nueva_clave = generar_contrasena_basica()
    
    print("-" * 30)
    print("GENERADOR DE CONTRASENAS")
    print("-" * 30)
    print(f"Tu nueva contraseña de 12 caracteres es: {nueva_clave}")
    print("-" * 30)