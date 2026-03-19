Prompt 1 

Genera el Readme.md del siguiente proyecto 

Este proyecto consiste en desarrollar un simulador de lanzamiento de dados interactivo en terminal quepermita al usuario elegir el tipo de dado (D4, D6, D8, D10, D12, D20), el número de dados a lanzar y las vecesque se repite la tirada. 

El simulador incluirá un historial de tiradas, estadísticas acumuladas (media, máximo, mínimo, total), unarepresentación visual de los resultados en la terminal usando barras de texto, y la posibilidad de guardar elhistorial en un archivo

Prompt 2

Vamos a ir haciéndolo paso a paso, solo haz lo que se pide en las tareas

Archivo:
src/simulador.py
Tareas:
● Importar el módulo random
● Crear función que simule el lanzamiento de un dado de 6 caras (D6)
● Mostrar el resultado del lanzamiento en la terminal con el símbolo del dado 🎲
● Ejecutar la función al iniciar el programa

Prompt 3

Archivo:
src/simulador.py
Tareas:
● Definir los tipos de dado disponibles: D4, D6, D8, D10, D12, D20
● Mostrar al usuario el menú de tipos de dado y pedirle que elija uno
● Adaptar la función de lanzamiento para usar el número de caras seleccionado
● Validar que la opción elegida sea válida; si no, mostrar error y pedir de nuevo