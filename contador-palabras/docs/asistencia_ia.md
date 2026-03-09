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