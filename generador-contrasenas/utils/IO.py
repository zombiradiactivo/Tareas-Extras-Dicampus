from datetime import datetime
from config.config import LONGITUD_MAX, LONGITUD_MIN, CANTIDAD_MAX, ARCHIVO_HISTORIAL


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

