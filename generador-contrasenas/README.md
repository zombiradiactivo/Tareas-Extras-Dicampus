# 🛡️ Generador de Contraseñas

Un generador de contraseñas robusto y seguro basado en terminal, diseñado en Python. Utiliza la criptografía de la librería secrets para garantizar que las claves generadas sean impredecibles y altamente seguras.
## ✨ Características Principales

- Generación Criptográficamente Segura: Utiliza el módulo secrets de Python en lugar de random, cumpliendo con estándares de seguridad para contraseñas.

- Personalización Total: Controla la longitud (8-128 caracteres), uso de mayúsculas, números y símbolos.

- Filtro de Caracteres Confusos: Opción para excluir caracteres visualmente similares como 0, O, l, I, 1 para evitar errores de lectura.

- Evaluador de Fortaleza: Análisis en tiempo real de la robustez de la contraseña (Débil, Media, Fuerte, Muy Fuerte).

- Historial Local: Opción para persistir las contraseñas generadas en un archivo contrasenas.txt con marca de tiempo.

## 🚀 Instalación y Uso
Requisitos Previos

- Tener instalado Python 3.6 o superior.

### Ejecución

Descarga o clona la carpeta https://github.com/zombiradiactivo/Tareas-Extras-Dicampus.git.

Abre una terminal en la carpeta Tareas-Extras-Dicampus / generador-contrasenas.

El proyecto tiene 3 versiones: 
### La base 
````Bash
python src/base_generador.py
````
### La refactorizada 
````Bash
python src/refactorizaodo_generador.py
````
### La modularizada
````Bash
python -m src.main
````

## 🛠️ Guía de Configuración

Al iniciar el programa, podrás configurar los siguientes parámetros:

| Parámetro | Rango / Opción | Descripción |
|--------|------------------|--------------------------------------|
| Longitud | 8 a 128 | Define el largo de la cadena (Recomendado: 16+). |
| Mayúsculas | s / n | Incluye caracteres de la A a la Z. |
| Números | s / n | Incluye dígitos del 0 al 9. |
| Símbolos | s / n | Incluye caracteres especiales (!@#$%...). |
| Excluir Confusos | s / n | Elimina caracteres que causan ambigüedad visual. |
| Cantidad | 1 a 10 | Número de contraseñas a generar por tanda. |


## 📊 Lógica de Evaluación de Fortaleza

El script no solo genera la clave, sino que la puntúa basándose en un sistema de 6 puntos de control:

- Longitud >= 8: +1 punto.

- Longitud >= 12: +1 punto adicional.

- Contiene Minúsculas: +1 punto.

- Contiene Mayúsculas: +1 punto.

- Contiene Números: +1 punto.

- Contiene Símbolos: +1 punto.

Resultados:

- 🔴 0-2 Puntos: Débil.

- 🟡 3 Puntos: Media.

- 🔵 4-5 Puntos: Fuerte.

- 🟢 6 Puntos: Muy Fuerte.

## 📝 Ejemplo de Salida
````Plaintext

=======================================================
      🛡️  GENERADOR DE CONTRASEÑAS  🛡️
=======================================================

--- 🛠️  Configuración de Seguridad ---
Longitud (8-128) [16]: 18
¿Incluir MAYÚSCULAS? (s/n) [Enter para sí]: s
¿Incluir Números? (s/n) [Enter para sí]: s
¿Incluir Símbolos especiales? (s/n) [Enter para sí]: s
¿Excluir caracteres confusos? (0, O, l, I, 1) (s/n) [Enter para sí]: s

¿Cuántas contraseñas quieres generar? (1-10) [Enter para 1]: 2

-------------------------------------------------------
  Caracteres disponibles tras filtrado: 89
🔑 2nxU7nXc|&gbc\}e3G        | ('Muy Fuerte 🛡️', 'VERDE')
  Caracteres disponibles tras filtrado: 89
🔑 vLjyx"A8UodsJ!-GY,        | ('Muy Fuerte 🛡️', 'VERDE')
-------------------------------------------------------

¿Deseas guardar estos resultados? (s/n) [Enter para sí]: s

✅ Guardado en contrasenas.txt

````

## 🛡️ Seguridad y Buenas Prácticas

  - Privacidad: El archivo contrasenas.txt se guarda localmente en tu equipo. Asegúrate de proteger este archivo o borrarlo después de usar las claves.

  - Entropía: Para máxima seguridad, se recomienda generar contraseñas de al menos 16 caracteres e incluir todos los tipos de símbolos.

## ✋😶🤚 Disclaimer

Este proyecto a sido creado con Inteligencia Artificial y revisado manualmente 

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. ¡Siéntete libre de usarlo, modificarlo y mejorarlo!