# Plataforma de inteligencia de datos para gastronomía vegana

Este proyecto desarrolla un **Dashboard analítico e interactivo** diseñado para consultores y dueños de restaurantes tradicionales. Su objetivo principal es mitigar el riesgo comercial y resolver el fenómeno del **"comensal veto"** (pérdida de grupos de clientes porque el local no ofrece opciones veganas reales) mediante la toma de decisiones basada en datos (*Data-Driven*).

La aplicación combina el procesamiento de datos estadísticos con una interfaz visual moderna para justificar la rentabilidad, optimizar costos de materias primas y analizar los precios de la competencia por región geográfica.

---

## 🛠️ Arquitectura y herramientas

El proyecto sigue una estructura estrictamente modular bajo el paradigma de **Programación Orientada a Objetos (POO)** e ingeniería de datos:

* **Lenguaje:** Python 3.12+
* **Procesamiento y Gobierno de Datos:** `Pandas` (con soporte del motor `lxml`) para la ingesta, limpieza, normalización y unificación de las fuentes mediante constantes de esquema.
* **Visualización Estática (Capa de Servidor):** `Matplotlib` y `Seaborn` para la generación automatizada de diagramas de cajas (márgenes) y regresiones lineales exportados dinámicamente en formato `base64`.
* **Visualización Interactiva y Frontend:** `Dash` y `Plotly Express` combinados con `dash_bootstrap_components` para una interfaz adaptativa bajo la guía de estilo *Eco-Clean*.

---

## 🚀 Guía de Instalación y Ejecución
Para desplegar este dashboard de manera local en tu entorno de desarrollo, ejecuta los siguientes comandos en tu terminal:

### 1. Clonar el repositorio
git clone https://github.com/SolMichelle/dashboard_gastrovegan
cd dashboard_gastrovegan

### 2. Crear y activar un entorno virtual
python -m venv venv
* En Windows: venv\Scripts\activate  | En Linux/Mac: source venv/bin/activate

### 3. Instalar las librerías requeridas
pip install -r requirements.txt

### 4. Iniciar la aplicación
python app.py

Una vez ejecutado, abre tu navegador web e ingresa a la dirección local: http://127.0.0.1:8050/
