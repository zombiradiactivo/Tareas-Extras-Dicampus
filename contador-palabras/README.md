# 📝 Contador de Palabras

Analizador de texto avanzado para terminal que proporciona métricas detalladas sobre la estructura y riqueza léxica de cualquier texto o archivo `.txt`.

## 🚀 Cómo empezar

### Requisitos
- Python 3.8 o superior.

### Instalación
1. Clona el repo.
2. No requiere librerías externas (solo módulos estándar).

### Ejecución
Opcion 1 (No modularizado)

```bash
python src/base_contador.py
```
Opcion 2 (Modularizado)
````bash
python -m src.main
````

## 📊 Métricas Incluidas

    Básicas: Conteo de palabras, caracteres, oraciones y párrafos.

    Léxicas: Riqueza léxica (%), longitud promedio de palabras.

    Frecuencia: Top 5 de palabras más usadas (filtrando conectores comunes).

    Extremos: Identificación de la palabra más larga y más corta.

## 🧪 Pruebas de Casos Borde (Edge Cases)

El sistema ha sido testeado para:

    Texto vacío: El programa informa que no hay contenido sin cerrarse.

    Solo números: Los números se tratan como tokens pero no afectan la riqueza léxica si no son palabras.

    Un solo carácter: Identificado correctamente como 1 palabra de longitud media 1.0.

    Archivos inexistentes: Manejo de excepciones con mensajes claros al usuario.

## 📂 Estructura

    src/: Código fuente.

    textos/: Archivos de entrada de ejemplo.

    docs/: Informes exportados y documentación.

    ultis/: Logica de analisis y logica de entrada / salida

    config/: Configuraciones (usadas para filtrar palabras frecuentes)

