from gui.main import GUI, top_level_reglas
from utils.utils import generar_eleccion_computadora
from utils.variables import REGLAS


class GameController:
    def __init__(self):
        # Instanciamos la interfaz
        self.view = GUI()
        
        # Inicializamos contadores internos
        self.victorias = 0
        self.derrotas = 0
        self.empates = 0

        
        # Configuramos los comandos de los botones de la GUI
        self.view.button_play.configure(command=self.procesar_jugada)
        self.view.button_reglas.configure(command=self.abrir_reglas)
        
        # Arrancamos la aplicación
        self.view.main.mainloop()

    def abrir_reglas(self):
        """Abre la ventana secundaria con la imagen de las reglas."""
        top_level_reglas()

    def procesar_jugada(self):
        """Maneja la lógica de combate y actualiza la interfaz."""
        # 1. Obtener elección del jugador desde el Combobox
        jugador = self.view.option_menu_var.get()
        
        if jugador == "Tipos" or not jugador:
            self.view.label_resultado.configure(text="¡Elige un tipo!", foreground="red")
            return

        # 2. Generar elección aleatoria de la CPU
        opciones = list(REGLAS.keys())
        cpu = generar_eleccion_computadora(opciones)
        
        # 3. Mostrar elección de la CPU en la interfaz
        self.view.label_seleccion_cpu_variable.configure(text=cpu)

        # 4. Determinar ganador según la lógica de Nivel 2 
        if jugador == cpu:
            resultado_texto = "¡EMPATE!"
            self.empates += 1
            color = "blue"
        elif cpu in REGLAS[jugador]:
            resultado_texto = "¡VICTORIA!"
            self.victorias += 1
            color = "green"
        else:
            resultado_texto = "DERROTA"
            self.derrotas += 1
            color = "red"

        # 5. Actualizar etiquetas de resultado y estadísticas
        self.view.label_resultado.configure(text=resultado_texto, foreground=color)
        self.view.label_victorias_variable.configure(text=str(self.victorias))
        self.view.label_derrotas_variable.configure(text=str(self.derrotas))
        self.view.label_empates_variable.configure(text=str(self.empates))
        self.view.label_porcentajes_variable.configure(text=str(f"{(self.victorias/(self.victorias + self.derrotas + self.empates))*100:.0f}%"))


if __name__ == "__main__":
    GameController()