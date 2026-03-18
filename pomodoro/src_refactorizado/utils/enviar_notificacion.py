from src_refactorizado.utils.emitir_sonido import emitir_sonido

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