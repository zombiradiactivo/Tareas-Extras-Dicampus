def calcular_propina(cuenta: float, porcentaje: float):

    porcentaje = porcentaje / 100
    propina = cuenta * porcentaje
    return propina



def divisor_cuenta(cuenta: float, propina: float, personas: int):
    
    cuenta_total = cuenta + propina
    cuenta_por_persona = cuenta_total / personas
    return cuenta_por_persona

## Test


def testing():
    cuenta = 0
    porcentaje =0
    personas = 0

    try:
        print("Introduce la cuenta (0.01-...):")
        cuenta = float(input())

        print("Introduce el porcentaje de la propina (0-...-33.3-...-100):")
        porcentaje = float(input())

        print("Introduce el numero de personas (1-...):")
        personas = int(input())

    except:
        raise RuntimeError("Se a ingresado un numero invalido")
        
    else:

        validaciones = {
        "La cuenta debe ser mayor a 0": cuenta > 0,                 ## Generado por IA
        "El porcentaje debe ser igual o mayor a 0": porcentaje >= 0,## Generado por IA
        "El porcentaje no puede exceder 100": porcentaje <= 100,    ## Generado por IA
        "Debe haber al menos 1 persona": personas >= 1              ## Generado por IA
        }


        if all(validaciones.values()):                              ## Generado por IA
            print(f"La propina de porcentaje {porcentaje}% es: ",calcular_propina(cuenta, porcentaje),"€")
            print(f"La cuenta por persona es de: ", divisor_cuenta(cuenta, calcular_propina(cuenta,porcentaje), personas),"€")
            testing()
        else:
            print(f"Has ingresado un numero invalido:")             
            for mensaje, estado in validaciones.items():            ## Generado por IA
                if not estado:                                      ## Generado por IA
                    print(f"- {mensaje}")                           ## Generado por IA
            testing()



testing()
