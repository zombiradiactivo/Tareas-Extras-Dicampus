def obtener_valor_validado(mensaje, default):
    """
    Tarea: Validar que los valores sean positivos y numéricos.
    """
    while True:
        entrada = input(f"{mensaje} (Presiona Enter para usar {default} min): ")
        if not entrada:
            return default
        
        try:
            valor = int(entrada)
            if valor > 0:
                return valor
            else:
                print("❌ El valor debe ser un número positivo (mayor a 0).")
        except ValueError:
            print("❌ Entrada no válida. Por favor, introduce un número entero.")
            
print("--- ⚙️ CONFIGURACIÓN DEL TEMPORIZADOR ---")