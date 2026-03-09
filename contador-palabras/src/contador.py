import sys
import os

def capturar_texto_terminal():
    """
    Pide al usuario introducir texto multilínea. 
    Se termina la captura dejando una línea en blanco (pulsando Enter dos veces).
    """
    print("\n--- Modo: Entrada Manual ---")
    print("Introduce el texto (Presiona ENTER en una línea vacía para finalizar):")
    
    lineas = []
    while True:
        linea = input()
        if linea == "":
            break
        lineas.append(linea)
    
    # Unimos las líneas con saltos de línea
    texto_final = "\n".join(lineas).strip()

    # Manejar el caso en que el usuario no introduzca nada
    if not texto_final:
        print("\n Error: No has introducido ningún texto.")
        return None

    # Mostrar el texto de vuelta para confirmación
    print("\n--- Texto Recibido ---")
    print(texto_final)
    print("----------------------")
    
    confirmar = input("\n¿Es correcto este texto? (s/n): ").lower()
    if confirmar == 's':
        return texto_final
    else:
        print("Operación cancelada por el usuario.")
        return None
    
if __name__ == "__main__":
    texto = capturar_texto_terminal()
    
    if texto:

        # Aquí llamarías a tus funciones de conteo
        print(f"Procesando {len(texto.split())} palabras...")

        texto_sin_doble_espacios = texto.replace('  ',' ')
        print(f"Numero de caracteres con espacios {len(texto_sin_doble_espacios)} espacios dobles cuentan como 1")

        texto_sin_espacios = texto_sin_doble_espacios.replace(' ','')
        print(f"Numero de caracteres sin espacios {len(texto_sin_espacios)}")