import os
import string
import secrets
from datetime import datetime

# --- CONSTANTES ---
LONGITUD_MIN = 8
LONGITUD_MAX = 128
CANTIDAD_MAX = 10
ARCHIVO_HISTORIAL = "contrasenas.txt"

# --- UTILIDADES ---

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo (Windows o Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    """Muestra el banner principal del programa con estilo visual."""
    limpiar_pantalla()
    print("="*55)
    print("      🛡️  GENERADOR DE CONTRASEÑAS  🛡️")
    print("="*55)

# --- LÓGICA  ---

def obtener_longitud():
    """
    Solicita y valida la longitud de la contraseña.
    
    Returns:
        int: Longitud validada entre LONGITUD_MIN y LONGITUD_MAX.
    """
    while True:
        entrada = input(f"Longitud ({LONGITUD_MIN}-{LONGITUD_MAX}) [16]: ").strip()
        if not entrada: return 16
        if entrada.isdigit():
            longitud = int(entrada)
            if LONGITUD_MIN <= longitud <= LONGITUD_MAX:
                return longitud
        print(f"❌ Error: Introduce un número entre {LONGITUD_MIN} y {LONGITUD_MAX}.")

def obtener_cantidad():
    """Valida que el usuario pida entre 1 y CANTIDAD_MAX contraseñas."""
    while True:
        entrada = input(f"\n¿Cuántas contraseñas quieres generar? (1-{CANTIDAD_MAX}) [Enter para 1]: ").strip()
        if not entrada: return 1
        try:
            cantidad = int(entrada)
            if 1 <= cantidad <= CANTIDAD_MAX:
                return cantidad
            print("❌ Por favor, elige un número entre 1 y 10.")
        except ValueError:
            print("❌ Error: Introduce un número entero válido.")

def obtener_si_no(mensaje):
    """
    Valida entradas de tipo sí/no (s/n).
    
    Args:
        mensaje (str): La pregunta a mostrar al usuario.
    Returns:
        bool: True para 's' o Enter, False para 'n'.
    """
    while True:
        respuesta = input(f"{mensaje} (s/n) [Enter para sí]: ").lower().strip()
        if respuesta == "" or respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("❌ Por favor, responde con 's' para sí o 'n' para no.")

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

def guardar_en_archivo(lista_passwords):
    """
    Escribe los resultados en el archivo local en modo append.
    
    Args:
        resultados (list): Lista de tuplas (password, fortaleza).
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as f:
            f.write(f"\n--- Sesión: {fecha_actual} ---\n")
            for pwd, fort in lista_passwords:
                f.write(f"[{fecha_actual}] PWD: {pwd} | Fortaleza: {fort}\n")
        print(f"\n✅ Guardado en {ARCHIVO_HISTORIAL}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")


# --- FUNCIONALIDADES DE MENÚ ---

def ver_historial():
    """Muestra el contenido del archivo de historial por pantalla."""
    limpiar_pantalla()
    print("--- 📜 HISTORIAL DE SEGURIDAD ---")
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("\nEl historial está vacío.")
    input("\nPresiona Enter para volver...")

def menu_generar():
    """Orquestador del proceso de configuración y muestra de resultados."""
    mostrar_bienvenida()
    print("\n--- 🛠️  Configuración de Seguridad ---")

    # Parámetros rápidos
    try:

        # 1. Obtener longitud
        longitud = obtener_longitud()


        # 2. Obtener preferencias de tipos
        # Nota: Si el usuario dice 'no' a todo, por defecto usaremos minúsculas
        mayus = obtener_si_no("¿Incluir MAYÚSCULAS?")
        nums = obtener_si_no("¿Incluir Números?")
        simbs = obtener_si_no("¿Incluir Símbolos especiales?")

        # Preguntar por exclusión de confusos
        excluir = obtener_si_no("¿Excluir caracteres confusos? (0, O, l, I, 1)")

        # 3. Generar y mostrar
        cantidad = obtener_cantidad()

    except ValueError:
        print("❌ Entrada inválida. Usando valores por defecto (Longitud 32)(Si a todo).")
        longitud, cantidad, mayus, nums, simbs, excluir = 32, 1, 1, 1, 1, 1


    resultados = []
    print("\n" + "-"*55)
    for _ in range(cantidad):
        pwd = generar_contrasena(longitud, mayus, nums, simbs, excluir)
        fort = evaluar_fortaleza(pwd)
        resultados.append((pwd, fort))
        print(f"🔑 {pwd:<25} | {fort}")
    print("-" * 55)

    if obtener_si_no("\n¿Deseas guardar estos resultados?"):
        guardar_en_archivo(resultados)
    
    input("\nPresiona Enter para continuar...")

# --- BUCLE PRINCIPAL ---

def main():
    """Bucle principal de la interfaz de usuario."""
    while True:
        mostrar_bienvenida()
        print("1. 🔑 Generar contraseña")
        print("2. 📜 Ver historial")
        print("3. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            menu_generar()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            print("\n¡Gracias por usar el Generador! Protege bien tus claves. 👋")
            break
        else:
            print("❌ Opción no válida.")
            input("Presiona Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()