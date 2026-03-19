from typing import Optional
class Multa:
    def __init__(self, id_alquiler: int, monto: float, pagada: bool = False, id: Optional[int] = None):
        self.id = id
        self.id_alquiler = id_alquiler
        self.monto = monto
        self.pagada = pagada

    def __str__(self):
        estado = "PAGADA" if self.pagada else "PENDIENTE"
        return f"Multa Ref:{self.id_alquiler} - Importe: {self.monto:.2f}€ [{estado}]"