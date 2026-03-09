Prompt 1 

Descripción del Ejercicio
Este proyecto consiste en desarrollar un generador de contraseñas seguras interactivo que permita al usuario crear contraseñas robustas según sus preferencias: longitud, uso de mayúsculas, minúsculas, números y símbolos especiales. 
El generador incluirá un sistema de evaluación de fortaleza de la contraseña generada (Débil / Media / Fuerte / Muy fuerte), opción de generar múltiples contraseñas a la vez y la posibilidad de guardarlas en un archivo de texto.

Estructura del Proyecto
generador-contrasenas/
│
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│ └── generador.py
└── docs/
└── asistencia_ia.md

● Crear README con descripción del proyecto y objetivos
● Crear requirements.txt (solo biblioteca estándar: string, secrets, os)

Prompt 2

● Importar los módulos string y secrets
● Crear función que genere una contraseña de 12 caracteres con todos los tipos
● Incluir letras minúsculas, mayúsculas, números y símbolos
● Mostrar la contraseña generada por pantalla

Prompt 3

● Modificar la función para aceptar la longitud como parámetro
● Preguntar al usuario la longitud deseada
● Establecer un valor por defecto de 16 caracteres
● Validar que la longitud sea un entero entre 8 y 128

Prompt 4

● Añadir parámetros opcionales: usar_mayusculas, usar_numeros, usar_simbolos
● Preguntar al usuario si quiere incluir cada tipo de carácter (s/n)
● Construir el conjunto de caracteres dinámicamente según las opciones
● Garantizar que al menos un tipo de carácter esté siempre activado

Prompt 5

● Crear función separada que evalúe la fortaleza de una contraseña
● Criterios: longitud, presencia de mayúsculas, minúsculas, números y símbolos
● Devolver una puntuación: Débil / Media / Fuerte / Muy fuerte
● Mostrar el resultado de la evaluación junto a la contraseña generada