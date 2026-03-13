from data.db import inicializar_db
from data.obtener_palabras import obtener_palabra_filtrada
from utils.dibujo import obtener_dibujo
from utils.selec_categoria import seleccionar_categoria


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
