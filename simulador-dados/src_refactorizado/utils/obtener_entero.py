def obtener_entero(msg, min_v, max_v):
    """
    Solicita una entrada numérica al usuario y la valida.

    Mantiene al usuario en un bucle hasta que proporcione un número entero
    dentro del rango especificado.

    Args:
        msg (str): El mensaje que se mostrará en el prompt.
        min_v (int): Valor mínimo aceptado.
        max_v (int): Valor máximo aceptado.

    Returns:
        int: El número validado proporcionado por el usuario.
    """
    while True:
        entrada = input(msg).strip()
        if entrada.isdigit() and min_v <= int(entrada) <= max_v:
            return int(entrada)
        print(f"❌ Error: Introduce un número entre {min_v} y {max_v}.")
