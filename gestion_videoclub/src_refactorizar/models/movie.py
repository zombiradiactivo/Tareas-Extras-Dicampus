from typing import Optional
class Pelicula:
    def __init__(self, titulo: str, director: str, copias_disponibles: int, id: Optional[int] = None):
        self.id = id
        self.titulo = titulo
        self.director = director
        self.copias_disponibles = copias_disponibles

    def __str__(self):
        status = "✅ Disponible" if self.copias_disponibles > 0 else "❌ Agotada"
        return f"[{self.id}] {self.titulo} - Dir: {self.director} ({self.copias_disponibles} copias) {status}"