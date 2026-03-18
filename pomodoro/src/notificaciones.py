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

def enviar_notificacion(titulo, mensaje, mensaje2=None):
    """
    Tarea: Mostrar mensaje visual destacado al cambiar de sesión.
    Maneja sistemas operativos para notificaciones (opcional) o banners.
    """
    # Tarea: Mensaje visual destacado en terminal
    ancho = 40
    print("\n" + "=" * ancho)
    print(f"{titulo.center(ancho)}")
    print("-" * ancho)
    print(f"{mensaje.center(ancho)}")
    if mensaje2:
        print("-" * ancho)
        print(f"{mensaje2.center(ancho)}")
    print("=" * ancho + "\n")
    
    # Emitir la alerta sonora
    emitir_sonido()

# Prueba rápida del módulo
if __name__ == "__main__":
    enviar_notificacion("PRUEBA", "El sistema de alertas funciona")