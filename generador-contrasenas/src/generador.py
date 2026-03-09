import string
import secrets

def generar_contrasena(longitud, incluir_mayus, incluir_nums, incluir_simb):
    """
    Construye la contraseña basándose en las preferencias del usuario.
    """
    # El set base siempre son minúsculas para garantizar que no esté vacío
    caracteres = string.ascii_lowercase
    
    if incluir_mayus:
        caracteres += string.ascii_uppercase
    if incluir_nums:
        caracteres += string.digits
    if incluir_simb:
        caracteres += string.punctuation

    # Generación segura
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def obtener_si_no(mensaje):
    """
    Valida entradas de tipo sí/no (s/n).
    """
    while True:
        respuesta = input(f"{mensaje} (s/n) [Enter para sí]: ").lower().strip()
        if respuesta == "" or respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("❌ Por favor, responde con 's' para sí o 'n' para no.")

def configurar_generacion():
    print("\n--- 🛠️  Configuración de Seguridad ---")
    
    # 1. Obtener longitud (reutilizando lógica previa)
    longitud = 16
    entrada_l = input("Longitud (8-128) [Enter para 16]: ").strip()
    if entrada_l:
        try:
            n = int(entrada_l)
            longitud = n if 8 <= n <= 128 else 16
        except ValueError:
            pass

    # 2. Obtener preferencias de tipos
    # Nota: Si el usuario dice 'no' a todo, por defecto usaremos minúsculas
    mayus = obtener_si_no("¿Incluir MAYÚSCULAS?")
    nums = obtener_si_no("¿Incluir Números?")
    simbs = obtener_si_no("¿Incluir Símbolos especiales?")

    # 3. Generar y mostrar
    password = generar_contrasena(longitud, mayus, nums, simbs)
    
    print("\n" + "="*40)
    print(f"✅ Tu contraseña personalizada:\n{password}")
    print("="*40)

if __name__ == "__main__":
    configurar_generacion()