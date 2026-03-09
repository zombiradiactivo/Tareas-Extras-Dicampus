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