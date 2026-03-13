from config.config import AHORCADO_ARTE


def obtener_dibujo(intentos_fallidos):
    """Retorna el arte ASCII correspondiente al número de errores."""
    if 0 <= intentos_fallidos < len(AHORCADO_ARTE):
        return AHORCADO_ARTE[intentos_fallidos]
    return AHORCADO_ARTE[-1]