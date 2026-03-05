# 🐍 Tip Calculator CLI (Python 3.14)

Una herramienta de línea de comandos eficiente y precisa para calcular propinas y dividir cuentas, desarrollada íntegramente en **Python**.

---

## 📖 Descripción

Este proyecto permite a los usuarios automatizar el cálculo de gratificaciones en establecimientos de servicios. Está diseñado para ser robusto, manejando errores de entrada (como valores no numéricos) y ofreciendo un desglose claro de los costos.

---

## ⚙️ Funcionalidades

* **Entrada de Datos Dinámica:** Monto de la factura, porcentaje de propina y número de personas.
* **Manejo de Excepciones:** Validación de entradas para evitar errores en tiempo de ejecución.
* **Formateo de Moneda:** Resultados redondeados a dos decimales para precisión financiera.
* **Lógica Matemática:**
    > El cálculo se basa en la fórmula estándar de servicios:
    > $$\text{Total Individual} = \frac{\text{Cuenta} \times (1 + \frac{\text{Propina}}{100})}{\text{Personas}}$$

---

## 🛠️ Requisitos e Instalación

Asegúrate de tener instalada la versión de **Python 3.14** o superior.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/zombiradiactivo/Tareas-Extras-Dicampus]
   cd calculadora-propinas
    ```
    (Opcional) Crear un entorno virtual:
    ```Bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
## 🚀 Ejecución

Para lanzar la calculadora, ejecuta el script principal desde tu terminal:
```Bash
python src/calculadora_propinas.py
```
