from datetime import date
from typing import Optional

class Alquiler:
    # Definimos la tarifa como una constante de clase (2.00€ por día de retraso)
    TARIFA_DIARIA_RETRASO = 2.0

    def __init__(self, id_cliente: int, id_pelicula: int, fecha_alquiler: date, 
                 fecha_prevista: date, fecha_entrega_real: Optional[date] = None, id: Optional[int] = None):
        self.id = id
        self.id_cliente = id_cliente
        self.id_pelicula = id_pelicula
        self.fecha_alquiler = fecha_alquiler
        self.fecha_prevista = fecha_prevista
        self.fecha_entrega_real = fecha_entrega_real

    def calcular_multa_actual(self) -> float:
        """
        Calcula la multa basándose en la fecha actual o la fecha en que se devolvió.
        """
        # Si ya se devolvió, usamos esa fecha; si no, usamos 'hoy' para ver la multa acumulada
        fecha_fin = self.fecha_entrega_real if self.fecha_entrega_real else date.today()
        
        if fecha_fin > self.fecha_prevista:
            dias_retraso = (fecha_fin - self.fecha_prevista).days
            return float(dias_retraso * self.TARIFA_DIARIA_RETRASO)
        
        return 0.0