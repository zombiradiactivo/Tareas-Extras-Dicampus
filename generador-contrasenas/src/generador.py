import string
import secrets
from datetime import datetime

def generar_contrasena(longitud, incluir_mayus, incluir_nums, incluir_simb, excluir_confusos):
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

    if excluir_confusos:
        confusos = "0OIl1"
        caracteres = "".join(c for c in caracteres if c not in confusos)
        print(f"  Caracteres disponibles tras filtrado: {len(caracteres)}")

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

def obtener_cantidad():
    """Valida que el usuario pida entre 1 y 10 contraseñas."""
    while True:
        entrada = input("\n¿Cuántas contraseñas quieres generar? (1-10) [Enter para 1]: ").strip()
        if not entrada: return 1
        try:
            cantidad = int(entrada)
            if 1 <= cantidad <= 10:
                return cantidad
            print("❌ Por favor, elige un número entre 1 y 10.")
        except ValueError:
            print("❌ Error: Introduce un número entero válido.")

def evaluar_fortaleza(password):
    """
    Evalúa la seguridad de la contraseña basada en criterios específicos.
    Retorna: (Puntuación, Categoría)
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

def guardar_en_archivo(lista_passwords):
    """Guarda las contraseñas generadas en un archivo de texto con timestamp."""
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("contrasenas.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- Sesión: {fecha_actual} ---\n")
            for pwd, fort in lista_passwords:
                f.write(f"[{fecha_actual}] PWD: {pwd} | Fortaleza: {fort}\n")
        print(f"\n✅ ¡Éxito! Las contraseñas se han guardado en 'contrasenas.txt'.")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")

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

    # Preguntar por exclusión de confusos
    excluir = obtener_si_no("¿Excluir caracteres confusos? (0, O, l, I, 1)")

    # 3. Generar y mostrar
    cantidad = obtener_cantidad()
    
    print("\n" + "="*50)
    print(f"{'N°':<4} | {'Contraseña':<20} | {'Fortaleza'}")
    print("-" * 50)
    
    resultados = [] # Lista para almacenar temporalmente y luego guardar
    for i in range(1, cantidad + 1):
        pwd = generar_contrasena(longitud, mayus, nums, simbs, excluir)
        fortaleza = evaluar_fortaleza(pwd)
        resultados.append((pwd, fortaleza))
        # Formateo de columnas para que se vea ordenado
        print(f"{i:<4} | {pwd:<20} | {fortaleza}")
        
    print("="*50)

    # Lógica de guardado solicitada
    if obtener_si_no("\n¿Deseas guardar estas contraseñas en un archivo?"):
        guardar_en_archivo(resultados)


if __name__ == "__main__":
    configurar_generacion()
    