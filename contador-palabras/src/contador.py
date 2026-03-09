import sys
import re
import os

def capturar_texto_terminal():
    """
    Pide al usuario introducir texto multilínea. 
    Se termina la captura dejando una línea en blanco (pulsando Enter dos veces).
    """
    print("\n--- Modo: Entrada Manual ---")
    print("Escribe tu texto. Para terminar, escribe la palabra 'FIN' en una línea nueva.")    

    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":  # Ahora termina con la palabra FIN
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
    
def contar_oraciones(texto):
    """
    Cuenta oraciones basándose en los delimitadores . ! y ?
    """
    if not texto.strip():
        return 0
    # Buscamos cualquier ocurrencia de los signos finales
    oraciones = re.findall(r'[^.!?]+[.!?]', texto)
    
    # Si el texto no termina en punto pero tiene contenido, contamos al menos 1
    return max(len(oraciones), 1 if texto.strip() else 0)

def contar_parrafos(texto):
    """
    Cuenta párrafos identificando bloques de texto separados por líneas vacías.
    """
    if not texto.strip():
        return 0
    # Dividimos por uno o más saltos de línea seguidos
    # \n{2,} detecta dos o más saltos de línea (una línea en blanco real)
    parrafos = re.split(r'\n\s*\n', texto.strip())
    return len(parrafos)

def mostrar_informe(texto):
    # Cálculos previos
    palabras = len(texto.split())
    caracteres = len(texto)
    caracteres_sin_espacios_dobles = texto.replace('  ',' ')
    texto_sin_espacios = caracteres_sin_espacios_dobles.replace(' ','')

    # Nuevos cálculos
    oraciones = contar_oraciones(texto)
    parrafos = contar_parrafos(texto)
    
    print("\n" + "="*30)
    print("📋 INFORME DE ANÁLISIS")
    print("="*30)
    print(f"🔹 Palabras:    {palabras}")
    print(f"🔹 Caracteres(con espacios):  {len(caracteres_sin_espacios_dobles)}")
    print(f"🔹 Caracteres(sin esapcios):  {len(texto_sin_espacios)}")    
    print(f"🔹 Oraciones:   {oraciones}")
    print(f"🔹 Párrafos:    {parrafos}")
    print("="*30 + "\n")

if __name__ == "__main__":
    texto = capturar_texto_terminal()
    
    if texto:


        mostrar_informe(texto)



        # # Aquí llamarías a tus funciones de conteo
        # print(f"Procesando {len(texto.split())} palabras...")

        # texto_sin_doble_espacios = texto.replace('  ',' ')
        # print(f"Numero de caracteres con espacios {len(texto_sin_doble_espacios)} espacios dobles cuentan como 1")

        # texto_sin_espacios = texto_sin_doble_espacios.replace(' ','')
        # print(f"Numero de caracteres sin espacios {len(texto_sin_espacios)}")