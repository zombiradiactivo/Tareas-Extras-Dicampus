from utils.IO import guardar_en_archivo, obtener_cantidad, obtener_longitud, obtener_si_no
from utils.utils import limpiar_pantalla, mostrar_bienvenida
from utils.generador import generar_contrasena
from utils.evaluador import evaluar_fortaleza
from config.config import ARCHIVO_HISTORIAL
import os


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
