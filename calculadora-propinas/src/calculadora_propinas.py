def calcular_propina(cuenta: float, porcentaje: float, divisa: bool, output: bool):

    porcentaje = porcentaje / 100
    propina = cuenta * porcentaje

    if divisa == output:
        return propina
    else:
        return conversor_divisa(divisa, propina)



def divisor_cuenta(cuenta: float, personas: int, divisa: bool, output: bool):

    cuenta_por_persona = cuenta / personas

    if divisa == output:
        return cuenta_por_persona
    else:
        return conversor_divisa(divisa, cuenta_por_persona)


def conversor_divisa(divisa, cantidad):
    ## 1 EUR equivale a 1,16 Dólar a dia de 06/03/2026

    # Cambio de € a $
    if divisa is False:
        cantidad = cantidad * 1.16
        return cantidad
    # Cambio de $ a €
    else:
        cantidad = cantidad - (cantidad * 0.16)
        return cantidad

## Test


def testing():
    divisa = 0
    cuenta = 0
    porcentaje =0
    personas = 0
    output = 0

    try:
        print("Elige la moneda €(0) o $(1) (0 - 1):")
        divisa = input()

        print("Introduce la cuenta (0.01 - ...):")
        cuenta = float(input())

        print("Introduce el porcentaje de la propina (0 - ... - 33.3 - ... - 100):")
        porcentaje = float(input())

        print("Introduce el numero de personas (1 - ...):")
        personas = int(input())

        print("Salida en €(0) o $(1) (0 - 1):")
        output = input()


    except:
        raise RuntimeError("Se a ingresado un numero invalido")
        
    else:

        validaciones = {
        "La entrada solo puede ser 0 o 1": divisa in ["0", "1"],
        "La salida solo puede ser 0 o 1": output in ["0", "1"],
        "La cuenta debe ser menor a 0": cuenta > 0,
        "El porcentaje debe ser igual o mayor a 0": porcentaje >= 0,
        "El porcentaje no puede exceder 100": porcentaje <= 100,
        "Debe haber al menos 1 persona": personas >= 1
        }


        if all(validaciones.values()):                              ## Generado por IA

            divisa = bool(int(divisa)) 
            print(divisa)
            output = bool(int(output)) 
            print(output)

            if output is False:
                tipo_moneda_caracter = "€"
            else:
                tipo_moneda_caracter = "$"

            propina_calculada = calcular_propina(cuenta, porcentaje, divisa, output)
            cuenta_dividida = propina_calculada + divisor_cuenta(cuenta, personas, divisa, output)

            print(f"La propina de porcentaje {porcentaje}% es: ",
                  f"{propina_calculada:.2f}",
                  f"{tipo_moneda_caracter}"
                  )
            
            print(f"La cuenta por persona es de: ", 
                  f"{cuenta_dividida:.2f}",
                  f"{tipo_moneda_caracter}"
                  )
            
            testing()
        else:
            print(f"Has ingresado un numero invalido:")             
            for mensaje, estado in validaciones.items():            ## Generado por IA
                if not estado:                                      ## Generado por IA
                    print(f"- {mensaje}")                           ## Generado por IA
            testing()



testing()
