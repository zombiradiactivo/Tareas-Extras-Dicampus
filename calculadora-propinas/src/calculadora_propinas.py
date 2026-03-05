def calcular_propina(cuenta: float, porcentaje):

    if porcentaje > 0:
        porcentaje = porcentaje / 100
        propina = cuenta * porcentaje
        return propina
    else:
        print("El porcentaje no puede ser negativo")


def divisor_cuenta(cuenta, propina, personas):
    
    cuenta_total = cuenta + propina
    cuenta_por_persona = cuenta_total / personas
    return cuenta_por_persona

## Test


def testing():

    print("Introduce la cuenta:")
    cuenta = float(input())
    print("Introduce el porcentaje de la propina:")
    porcentaje = float(input())
    print("Introduce el numero de personas:")
    personas = int(input())

    print(f"La propina de porcentaje {porcentaje}% es: ",calcular_propina(cuenta, porcentaje),"€")
    print(f"La cuenta por persona es de: ", divisor_cuenta(cuenta, calcular_propina(cuenta,porcentaje), personas),"€")

testing()
