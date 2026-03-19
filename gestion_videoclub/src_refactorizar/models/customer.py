from typing import Optional
class Cliente:
    def __init__(self, nombre: str, email: str, id: Optional[int] = None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.historial_alquileres = [] # Se cargará desde el service cuando sea necesario

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', email='{self.email}')"