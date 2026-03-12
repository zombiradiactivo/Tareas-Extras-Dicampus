# 1. Inicialización de variables (Marcador)
victorias = 0
derrotas = 0
empates = 0


REGLAS = {
    "Human": ["Tree", "Wolf", "Sponge", "Paper", "Air", "Water", "Dragon"],
    "Tree": ["Wolf", "Sponge", "Paper", "Air", "Water", "Dragon", "Devil"],
    "Wolf": ["Sponge", "Paper", "Air", "Water", "Dragon", "Devil", "Lightning"], 
    "Sponge": ["Paper", "Air", "Water", "Dragon", "Devil", "Lightning", "Gun"], 
    "Paper": ["Air", "Water", "Dragon", "Devil", "Lightning", "Gun", "Rock"],
    "Air": ["Water", "Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire"], 
    "Water": ["Dragon", "Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors"], 
    "Dragon": ["Devil", "Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake"], 
    "Devil": ["Lightning", "Gun", "Rock", "Fire", "Scissors", "Snake", "Human"], 
    "Lightning": ["Gun", "Rock", "Fire", "Scissors", "Snake", "Human", "Tree"], 
    "Gun": ["Rock", "Fire", "Scissors", "Snake", "Human", "Tree", "Wolf"], 
    "Rock": ["Fire", "Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge"], 
    "Fire": ["Scissors", "Snake", "Human", "Tree", "Wolf", "Sponge", "Paper"], 
    "Scissors": ["Snake", "Human", "Tree", "Wolf", "Sponge", "Paper", "Air"], 
    "Snake": ["Human", "Tree", "Wolf", "Sponge", "Paper", "Air", "Water"] 
}


def actualizar_marcador(resultado, v, d, e):
    """
    Actualiza los contadores globales basándose en el resultado de la ronda.
    """
    if resultado == "Victoria":
        v += 1
    elif resultado == "Derrota":
        d += 1
    else:
        e += 1
    return v, d, e

def mostrar_estadisticas(v, d, e):
    """
    Muestra el marcador actual de forma visual en la terminal.
    """
    print("\n" + "="*30)
    print(f"📊 MARCADOR ACTUAL:")
    print(f"🏆 Victorias: {v}")
    print(f"💀 Derrotas:  {d}")
    print(f"🤝 Empates:   {e}")
    print(f"Porcentaje Victorias:   {(v/(v + d + e))*100:.0f}%")

    print("="*30 + "\n")
