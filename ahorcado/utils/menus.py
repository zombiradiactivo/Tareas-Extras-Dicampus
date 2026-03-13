from src.ahorcado import jugar
from data.db import inicializar_db
from data.insertar_palabra import insertar_palabra
from data.obtener_palabras import obtener_todas_las_palabras
from utils.validador import limpiar_entrada, validar_nueva_palabra


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
