from validaciones import validar_nueva_palabra, limpiar_entrada
from base_datos import inicializar_db, conectar, insertar_palabra, obtener_todas_las_palabras, obtener_estadisticas_categorias, obtener_palabra_filtrada
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
    """
    Funcion principal de la logica de juego
    """

    # Asegurar que existan datos
    inicializar_db()
    
    cat_elegida = seleccionar_categoria()
    
    datos = obtener_palabra_filtrada(cat_elegida)

    # datos = obtener_palabra_aleatoria()
    if not datos:
        print("Error: No hay palabras en la base de datos.")
        return

    palabra_objetivo = datos[0].upper()
    categoria = datos[1]
    
    letras_adivinadas = set()
    intentos_fallidos = 0
    MAX_INTENTOS = 6

    print(f"--- BIENVENIDO AL AHORCADO ---")
    print(f"\n¡Juego iniciado! Categoría: {categoria}")

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

def seleccionar_categoria():
    """Muestra categorías y permite al usuario elegir una."""
    stats = obtener_estadisticas_categorias()
    
    print("\n--- CATEGORÍAS DISPONIBLES ---")
    print(f"{'#':<3} {'Categoría':<20} {'Palabras':<10}")
    print("-" * 35)
    
    categorias_lista = []
    for i, (nombre, total) in enumerate(stats, 1):
        print(f"{i:<3} {nombre:<20} {total:<10}")
        categorias_lista.append(nombre)
    
    print(f"{len(categorias_lista) + 1}: Todas (Aleatorio)")

    try:
        seleccion = int(input("\nSelecciona el número de categoría: "))
        if 1 <= seleccion <= len(categorias_lista):
            return categorias_lista[seleccion - 1]
        else:
            return None # Opción "Todas"
    except ValueError:
        print("Entrada no válida. Se elegirá una categoría al azar.")
        return None

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
    
    entrada_usuario = input("Introduce la nueva palabra o frase: ")
    
    # 1. Validar formato
    es_valida, resultado = validar_nueva_palabra(entrada_usuario)
    
    if es_valida:
        palabra_final = resultado # Ya viene en minúsculas y sin espacios locos
        cat = limpiar_entrada(input("Categoría: "))
        dif = limpiar_entrada(input("Dificultad: "))
        
        # 2. Intentar guardar
        exito, mensaje = insertar_palabra(palabra_final, cat, dif)
        print(mensaje)
    else:
        print(resultado) # Imprime el error de validación

if __name__ == "__main__":
    menu_principal()