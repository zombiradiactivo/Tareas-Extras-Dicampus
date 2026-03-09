import string
import secrets

def generar_contrasena(longitud=16):
    """
    Genera una contraseña segura combinando todos los tipos de caracteres.
    """
    caracteres = string.ascii_letters + string.digits + string.punctuation
    # Usamos secrets.choice para una selección criptográficamente segura
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

def obtener_longitud_valida():
    """
    Solicita y valida la entrada del usuario para la longitud.
    """
    while True:
        entrada = input("\nIntroduce la longitud deseada (8-128) [Presiona Enter para 16]: ").strip()
        
        # Si el usuario solo presiona Enter, usamos el valor por defecto
        if not entrada:
            return 16
        
        # Validamos que sea un número y esté en el rango
        try:
            n = int(entrada)
            if 8 <= n <= 128:
                return n
            else:
                print("❌ Error: La longitud debe estar entre 8 y 128.")
        except ValueError:
            print("❌ Error: Por favor, introduce un número entero válido.")

# --- Bloque Principal ---
if __name__ == "__main__":
    print("--- 🔐 Configuración de tu Contraseña Segura ---")
    
    # Obtenemos la longitud validada
    largo = obtener_longitud_valida()
    
    # Generamos y mostramos el resultado
    password = generar_contrasena(largo)
    
    print("\n" + "="*40)
    print(f"✅ Tu contraseña generada es:\n{password}")
    print("="*40)