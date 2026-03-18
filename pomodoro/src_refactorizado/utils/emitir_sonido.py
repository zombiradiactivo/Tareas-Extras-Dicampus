import os
import platform

def emitir_sonido():
    """
    Tarea: Emitir sonido al terminar cada sesión (beep de terminal).
    Maneja diferentes sistemas operativos.
    """
    sistema = platform.system()
    
    try:
        if sistema == "Windows":
            import winsound
            # Frecuencia 1000Hz, Duración 500ms
            winsound.Beep(1000, 500)
        elif sistema == "Darwin":  # macOS
            os.system('say "Tiempo terminado"')
            print("\a") # Bell character
        else:  # Linux y otros
            print("\a")
    except Exception:
        # Si falla el sonido, al menos imprimimos un aviso visual
        print("🔔 [SONIDO]")
