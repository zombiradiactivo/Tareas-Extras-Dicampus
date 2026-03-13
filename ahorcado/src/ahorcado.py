import random
from base_datos import conectar

def obtener_palabra_aleatoria():
    """Selecciona una palabra al azar de la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Usamos ORDER BY RANDOM() de SQLite para eficiencia en tablas pequeñas
    cursor.execute("SELECT palabra, categoria, dificultad FROM palabras ORDER BY RANDOM() LIMIT 1")
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return {
            "palabra": resultado[0].upper(),
            "categoria": resultado[1],
            "dificultad": resultado[2]
        }
    return None

def mostrar_progreso(palabra, letras_adivinadas):
    """
    Genera la representación visual de la palabra (p. ej. A _ O _ C A _ O).
    """
    representacion = ""
    for letra in palabra:
        if letra in letras_adivinadas:
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


# Test
if __name__ == "__main__":
    # Inicialización
    datos_palabra = obtener_palabra_aleatoria()
    if datos_palabra is not None:
        palabra_objetivo = datos_palabra['palabra']
        letras_usadas = set() # Usamos un set para evitar duplicados y búsquedas rápidas

        print(f"Categoría: {datos_palabra['categoria']}")
        print(f"Progreso: {mostrar_progreso(palabra_objetivo, letras_usadas)}")

        # Ejemplo de un turno:
        letra_usuario = "A" # Supongamos que viene de un input()
        if gestionar_intento(letra_usuario, letras_usadas):
            if letra_usuario in palabra_objetivo:
                print("¡Acertaste!")
            else:
                print("Letra incorrecta.")

        print(f"Letras intentadas: {', '.join(sorted(letras_usadas))}")
    else:
        print("❌ Error: No se encontraron palabras en la base de datos.")