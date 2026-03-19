import random

def lanzar_d6():
    """
    Simula el lanzamiento de un dado de 6 caras y muestra el resultado.
    """
    resultado = random.randint(1, 6)
    print(f"🎲 Resultado del lanzamiento: {resultado}")

if __name__ == "__main__":
    lanzar_d6()