Prompt 1

Crear README con descripción del proyecto

Este proyecto consiste en desarrollar el clásico Juego del Ahorcado con una base de datos
SQLite que almacena el diccionario de palabras. El jugador deberá adivinar letras de una
palabra oculta antes de agotar sus intentos. La aplicación permitirá consultar palabras
existentes y añadir nuevas palabras a la base de datos. 

Prompt 2

Tareas:
• Crear conexión con SQLite usando sqlite3
• Crear tabla 'palabras' con campos: id, palabra, categoria, dificultad
• Insertar al menos 20 palabras iniciales en la BD
• Crear función para ver todas las palabras almacenadas

Prompt 3

Tareas:
• Crear función que obtenga una palabra aleatoria de la BD
• Mostrar la palabra oculta como guiones bajos (p.ej. _ _ _ _ _)
• Registrar qué letras ya han sido adivinadas

Prompt 4

Tareas:
• Capturar letra ingresada por el usuario
• Comprobar si la letra está en la palabra
• Actualizar la palabra oculta revelando letras correctas
• Llevar contador de intentos fallido

Prompt 5

Tareas:
• Crear lista con los 7 estados del ahorcado en arte ASCII 
• Mostrar el estado correspondiente según los intentos fallidos
• Mostrar letras incorrectas usadas hasta el momento

Prompt 6 

Tareas:
• Detectar cuando el jugador ha adivinado todas las letras (victoria)
• Detectar cuando se han agotado los 6 intentos (derrota)
• Mostrar mensaje de resultado y revelar la palabra completa
• Preguntar si desea jugar otra partida

Prompt 7 

Tareas:
• Crear función para insertar una nueva palabra en la BD
• Solicitar al usuario: palabra, categoría y dificultad
• Verificar que la palabra no exista ya en la base de datos
• Confirmar al usuario que la palabra fue añadida correctamente

Prompt 8

Tareas:
• Validar que la letra ingresada sea solo una letra del alfabeto
• Validar que la nueva palabra solo contenga letras (sin números ni símbolos)
• Manejar errores de la BD con try-except
• Convertir entradas a minúsculas automáticamente

Prompt 9

Tareas:
• Mostrar las categorías disponibles en la BD
• Permitir al usuario elegir categoría antes de empezar
• Filtrar la consulta SQLite por categoría y/o dificultad
• Mostrar cuántas palabras hay disponibles por categoría