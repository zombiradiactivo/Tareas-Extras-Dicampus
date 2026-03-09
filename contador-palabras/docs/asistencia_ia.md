🤖 Registro de Asistencia de IA

Proyecto: Contador de Palabras
Objetivo: Crear una herramienta CLI para análisis de texto.

Prompts utilizados:

    Generación de estructura de archivos y README.

    Implementación de captura multilínea con delimitadores.

    Lógica de conteo con Regex (re) para oraciones y párrafos.

    Análisis de frecuencia con collections.Counter y filtrado de stop-words.

    Cálculo de métricas avanzadas (riqueza léxica, longitud media).

    Gestión de errores en lectura/escritura de archivos.

    Interfaz de usuario dinámica (limpieza de pantalla y bucle de menú).


Prompt 1

Genera el readme.md de el siguiente proyecto 

El programa permitirá analizar tanto texto introducido directamente en la terminal como texto cargado desde un
archivo .txt externo, mostrando un informe completo y guardando los resultados si el usuario lo desea.

Estructura proyecto
````
contador-palabras/
│
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│ └── contador.py
├── textos/
│ └── ejemplo.txt
└── docs/
└── asistencia_ia.md 

````

Prompt 2 

● Crear función que pida al usuario que introduzca un texto en la terminal
● Permitir introducir varias líneas usando un delimitador (ej: línea vacía para terminar)
● Mostrar el texto introducido de vuelta al usuario para confirmarlo
● Manejar el caso en que el usuario no introduzca nada

Prompt 3 

● Importar Counter del módulo collections
● Crear función que liste las N palabras más frecuentes del texto
● Ignorar mayúsculas y minúsculas al contar (convertir todo a lower())
● Filtrar palabras vacías comunes: 'el', 'la', 'de', 'que', 'y', 'en', 'a', 'un'
● Mostrar el TOP 5 de palabras con su número de apariciones

Prompt 4 

● Calcular la longitud media de las palabras del texto
● Contar el número de palabras únicas (sin repeticiones)
● Calcular el porcentaje de palabras únicas sobre el total
● Identificar la palabra más larga y la más corta del texto
● Mostrar todas las estadísticas en un bloque de resultados bien formateado

Prompt 5

● Crear el archivo textos/ejemplo.txt con un texto de prueba de varias líneas
● Crear función que cargue y lea un archivo .txt dado su ruta
● Aplicar todas las funciones de análisis ya creadas al texto del archivo
● Manejar errores: archivo no encontrado, archivo vacío, ruta incorrecta

Prompt 6

● Preguntar al usuario si quiere guardar el informe de análisis
● Crear función que escriba todos los resultados en un archivo informe.txt
● Incluir en el informe: fecha, hora, fuente del texto y todas las estadísticas
● Confirmar al usuario la ruta donde se ha guardado el archivo

Prompt 7

● Agregar docstrings a todas las funciones siguiendo PEP 257
● Refactorizar el código: cada función hace una sola cosa (principio SRP)
● Revisar y completar el README con instrucciones de uso y ejemplos de ejecución
● Crear el archivo docs/asistencia_ia.md documentando todos los prompts usados con IA
● Probar todos los casos edge: texto vacío, un solo carácter, texto con solo números