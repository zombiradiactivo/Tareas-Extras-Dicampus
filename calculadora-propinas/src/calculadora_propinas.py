def calcular_propina_10_fijo(cuenta: float):
    propina = cuenta * 0.1
    return propina

## Test

print("La propina fija del 10% es: ",calcular_propina_10_fijo(100),"€")