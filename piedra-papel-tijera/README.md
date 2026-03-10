# Piedra, Papel, Tijeras, Lagarto, Spock - Nivel 2
## 📝 Descripción del Proyecto

Este proyecto es una versión extendida y avanzada del clásico juego "Piedra, Papel o Tijeras". Consiste en un simulador interactivo por terminal donde un jugador humano se enfrenta a la computadora bajo un sistema de reglas de Nivel 2, que expande significativamente las posibilidades de combate.

El juego incluye:

    Interfaz clara y amigable en la terminal.

    Sistema de puntuación por partidas.

    Estadísticas detalladas de la sesión de juego.

    Lógica de enfrentamiento basada en una matriz de 15 variantes.

## ⚖️ Reglas del Juego (Nivel 2)

En esta modalidad, cada elemento vence a otros 7 elementos específicos. A continuación se detalla la tabla de victorias para cada elección:
|Elemento	| Vence a... |
|---------|-----------|
|Human       | Tree, Wolf, Sponge, Paper, Air, Water, Dragon |
|Tree	    | Wolf, Sponge, Paper, Air, Water, Dragon, Devil |
|Wolf	    | Sponge, Paper, Air, Water, Dragon, Devil, Lightning |
|Sponge	    | Paper, Air, Water, Dragon, Devil, Lightning, Gun |
|Paper	    | Air, Water, Dragon, Devil, Lightning, Gun, Rock |
|Air	        | Water, Dragon, Devil, Lightning, Gun, Rock, Fire |
|Water	    | Dragon, Devil, Lightning, Gun, Rock, Fire, Scissors |
|Dragon	    | Devil, Lightning, Gun, Rock, Fire, Scissors, Snake |
|Devil	    | Lightning, Gun, Rock, Fire, Scissors, Snake, Human |
|Lightning	| Gun, Rock, Fire, Scissors, Snake, Human, Tree |
|Gun	   | Rock, Fire, Scissors, Snake, Human, Tree, Wolf |
|Rock	    | Fire, Scissors, Snake, Human, Tree, Wolf, Sponge |
|Fire	    | Scissors, Snake, Human, Tree, Wolf, Sponge, Paper |
|Scissors	| Snake, Human, Tree, Wolf, Sponge, Paper, Air |
|Snake	    | Human, Tree, Wolf, Sponge, Paper, Air, Water |
🚀 Cómo Jugar

    Inicio: Al ejecutar el script, se te presentarán las opciones disponibles.

    Elección: Introduce el nombre del elemento que deseas jugar.

    Resultado: La computadora elegirá una opción al azar y se determinará el ganador según la tabla anterior.

    Estadísticas: Podrás ver el acumulado de victorias, derrotas y empates durante tu sesión.