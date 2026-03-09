# Generador de Contraseñas Seguras Interactivo

## Descripción
Este proyecto es una herramienta de línea de comandos diseñada para generar contraseñas robustas y personalizadas. Permite al usuario definir criterios específicos de seguridad y evaluar la fortaleza de las claves generadas.

## Características principales
* **Personalización total:** Elige longitud y tipos de caracteres (Mayúsculas, minúsculas, números, símbolos).
* **Seguridad Criptográfica:** Uso del módulo `secrets` de Python para garantizar aleatoriedad real.
* **Evaluador de Fortaleza:** Sistema que clasifica la contraseña como Débil, Media, Fuerte o Muy Fuerte.
* **Modo Batch:** Generación de múltiples contraseñas de forma simultánea.
* **Persistencia:** Opción para exportar las contraseñas generadas a un archivo `.txt`.

## Requisitos
* Python 3.6 o superior.
* No requiere dependencias externas (usa la biblioteca estándar).

## Instalación y Uso
1. Clona el repositorio.
2. Navega a la carpeta `src/`.
3. Ejecuta el programa con: `python generador.py`