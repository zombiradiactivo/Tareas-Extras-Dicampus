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

Prompt 4

Archivo:
src/simulador.py
Tareas:
● Preguntar al usuario cuántos dados quiere lanzar (1 a 10)
● Lanzar todos los dados de una vez y mostrar cada resultado individualmente
● Mostrar también la suma total de todos los dados lanzados
● Validar que el número de dados sea un entero entre 1 y 10

Prompt 5

Archivo:
src/simulador.py
Tareas:
● Preguntar al usuario cuántas veces quiere repetir la tirada (1 a 20)
● Ejecutar todas las tiradas en un bucle y almacenar los resultados en una lista
Módulo 2 · Estrategias de Generación de Código con IA · Dicampus
● Mostrar cada tirada numerada con sus dados y su suma parcial
● Calcular y mostrar la suma global de todas las tiradas

Prompt 6 

Archivo:
src/simulador.py
Tareas:
● Crear función que calcule estadísticas sobre todas las tiradas de la sesión
● Calcular: suma total, media por tirada, valor máximo y valor mínimo obtenidos
● Mostrar las estadísticas al final de cada serie de lanzamientos
● Identificar en qué tirada se obtuvo el resultado más alto y el más bajo

Prompt 7 

Archivo:
src/simulador.py
Tareas:
● Crear función que muestre un histograma de barras en la terminal usando el carácter ■
● Representar la frecuencia de cada valor posible del dado en las tiradas realizadas
● Escalar las barras proporcionalmente al valor más frecuente
● Mostrar el histograma tras cada serie de tiradas