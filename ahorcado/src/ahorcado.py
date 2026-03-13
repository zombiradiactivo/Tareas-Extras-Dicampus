import os
from base_datos import inicializar_db, conectar, insertar_palabra, obtener_todas_las_palabras
from dibujo import obtener_dibujo
# from validaciones import validar_letra # Todavia no implementado

def obtener_palabra_aleatoria():
    """Selecciona una palabra al azar de la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra, categoria FROM palabras ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()
    return resultado # Retorna (palabra, categoria) o None

def mostrar_progreso(palabra, letras_adivinadas):
    """
    Genera la representación visual de la palabra (p. ej. A _ O _ C A _ O).
    """
    representacion = ""
    for letra in palabra:
        if letra == " ":
            representacion += "    "  # Doble espacio para separar palabras
        elif letra in letras_adivinadas:
            representacion += f"{letra} "
        else:
            representacion += "_ "
    return representacion.strip()

def gestionar_intento(letra, letras_adivinadas):
    """
    Registra la letra y verifica si ya fue intentada.
    Retorna True si es una letra nueva, False si ya se había dicho.
    """
    letra = letra.upper()
    if letra in letras_adivinadas:
        print(f"⚠️ Ya intentaste con la letra '{letra}'. Prueba otra.")
        return False
    
    letras_adivinadas.add(letra)
    return True


def jugar():
    # Asegurar que existan datos
    inicializar_db()
    
    datos = obtener_palabra_aleatoria()
    if not datos:
        print("Error: No hay palabras en la base de datos.")
        return

    palabra_objetivo = datos[0].upper()
    categoria = datos[1]
    
    letras_adivinadas = set()
    intentos_fallidos = 0
    MAX_INTENTOS = 6

    print(f"--- BIENVENIDO AL AHORCADO ---")
    print(f"Categoría: {categoria}")

    while intentos_fallidos < MAX_INTENTOS:
        # 1. Mostrar palabra oculta (p.ej. _ _ A _ _)
        progreso = [letra if letra in letras_adivinadas else "_" for letra in palabra_objetivo]
        print(f"\nPalabra: {' '.join(progreso)}")
        print(f"Intentos fallidos: {intentos_fallidos}/{MAX_INTENTOS}")
        print(f"Letras usadas: {', '.join(sorted(letras_adivinadas))}")

        # 2. Capturar letra
        entrada = input("Introduce una letra: ").upper()

        # Validación básica (puedes mover esto a validaciones.py)
        if len(entrada) != 1 or not entrada.isalpha():
            print("❌ Por favor, introduce solo una letra válida.")
            continue

        if entrada in letras_adivinadas:
            print(f"⚠️ Ya habías dicho la '{entrada}'.")
            continue

        # 3. Registrar letra y comprobar
        letras_adivinadas.add(entrada)

        if entrada in palabra_objetivo:
            print(f"✅ ¡Bien hecho! La '{entrada}' está en la palabra.")
        else:
            intentos_fallidos += 1
            print(obtener_dibujo(intentos_fallidos))
            print(f"❌ La letra '{entrada}' no está. Pierdes un intento.")
            

        # 4. Comprobar victoria
        letras_sin_espacios = [l for l in palabra_objetivo if l != " "]

        if all(l in letras_adivinadas for l in letras_sin_espacios):
            print(f"\n✨ ¡VICTORIA! Has adivinado la frase: {palabra_objetivo}")
            return True
    if intentos_fallidos >= MAX_INTENTOS:
        print(f"\n💥 ¡OH NO! Has sido ahorcado. La palabra era: {palabra_objetivo}")

def menu_principal():
    """Controla el flujo de reinicio del juego."""
    # Aseguramos que la DB tenga datos al arrancar
    inicializar_db()
    while True:
            print("\n--- JUEGO DEL AHORCADO ---")
            print("1. Jugar partida")
            print("2. Ver diccionario")
            print("3. Añadir nueva palabra")
            print("4. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                jugar()
            elif opcion == "2":
                obtener_todas_las_palabras() # Función que creamos al inicio
            elif opcion == "3":
                menu_añadir_palabra()
            elif opcion == "4":
                print("¡Adiós!")
                break
            else:
                print("Opción no válida.")


def menu_añadir_palabra():
    """Interfaz para capturar datos de una nueva palabra."""
    print("\n--- AÑADIR NUEVA PALABRA ---")
    
    palabra = input("Ingresa la palabra: ").strip()
    if not all(char.isalpha() or char.isspace() for char in palabra):
        print("❌ Error: La palabra solo debe contener letras.")
        return

    categoria = input("Ingresa la categoría (ej. Cine, Frutas): ").strip()
    print("Dificultades disponibles: Fácil, Media, Difícil")
    dificultad = input("Ingresa la dificultad: ").strip()

    if not palabra or not categoria or not dificultad:
        print("❌ Error: Todos los campos son obligatorios.")
        return

    # Llamada a la función de base de datos
    exito, mensaje = insertar_palabra(palabra, categoria, dificultad)
    
    if exito:
        print(f"✅ {mensaje}")
    else:
        print(f"⚠️ {mensaje}")

if __name__ == "__main__":
    menu_principal()