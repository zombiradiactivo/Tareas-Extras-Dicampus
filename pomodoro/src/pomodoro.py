import time
import os

def cuenta_regresiva(segundos):
    """
    Función que realiza la cuenta regresiva y muestra el tiempo
    restante en formato MM:SS en la terminal.
    """
    while segundos >= 0:
        # Tarea: Calcular minutos y segundos
        minutos, segs = divmod(segundos, 60)
        
        # Tarea: Mostrar el tiempo restante en formato MM:SS
        # El uso de \r permite que el tiempo se actualice en la misma línea
        tiempo_formateado = f"{minutos:02d}:{segs:02d}"
        print(f"Tiempo restante: {tiempo_formateado}", end="\r")
        
        time.sleep(1)
        segundos -= 1
    
    print("\n¡Tiempo completado!")

# Tarea: Probar manualmente con 1 minuto (60 segundos)
if __name__ == "__main__":
    print("Iniciando prueba de 1 minuto...")
    cuenta_regresiva(60)