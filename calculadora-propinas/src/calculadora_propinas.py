def calcular_propina(cuenta: float, porcentaje):

    if porcentaje > 0:
        porcentaje = porcentaje / 100
        print(porcentaje)
        propina = cuenta * porcentaje
        return propina
    else:
        print("El porcentaje no puede ser negativo")

## Test


def testing():

    print("Introduce la cuenta:")
    cuenta = float(input())
    print("Introduce el porcentaje de la propina:")
    porcentaje = float(input())

    print(f"La propina de porcentaje {porcentaje}% es: ",calcular_propina(cuenta,porcentaje),"€")

testing()
