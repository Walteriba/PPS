
# 🚀 Puesta en marcha de un proyecto Flask

¡Bienvenido! Esta guía te ayudará a configurar y ejecutar el proyecto en tu entorno local.

## 📋 Requisitos previos

Asegúrate de tener instalados los siguientes programas:

- **Python 3.x:** [Descargar](https://www.python.org/downloads/)
- **Pip:** (Normalmente viene con Python)

## 🛠️ Instalación

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Walteriba/PPS.git
    cd PPS
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # Crea el entorno
    python -m venv venv

    # Actívalo
    # En Linux/Mac:
    source venv/bin/activate
    # En Windows:
    venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    > **Nota para PostgreSQL**: Si planeas usar PostgreSQL como base de datos, asegúrate de que el driver esté en `requirements.txt` y se instale.
    > ```bash
    > pip install psycopg2-binary
    > ```

## ⚙️ Ejecución

Una vez instalado, puedes ejecutar la aplicación:

1.  **Configura la aplicación Flask:**
    ```bash
    # En Linux/Mac:
    export FLASK_APP=app.py
    # En Windows:
    set FLASK_APP=app.py
    ```

2.  **Inicia el servidor de desarrollo:**
    ```bash
    flask run --debug
    ```
    El modo `--debug` reiniciará el servidor automáticamente con cada cambio.

3.  **¡Listo!** Abre tu navegador y ve a [http://localhost:5000](http://localhost:5000).

## 🗃️ Base de datos

El proyecto incluye un script para cargar datos de prueba en la base de datos.

1.  **Ejecuta el script:**
    (Asegúrate de estar en la raíz del proyecto)
    ```bash
    python -m utils.cargar_db
    ```

## 🔐 Configuración de Variables de Entorno

1. **Crea un archivo `.env` en la raíz del proyecto:**
   ```bash
   touch .env
   ```

2. **Añade las siguientes variables en el archivo `.env`:**
   ```bash
   # Clave secreta para sesiones y seguridad (REQUERIDA)
   # Genera una clave segura y única para tu entorno
   SECRET_KEY=tu-clave-secreta-aqui-muy-larga-y-aleatoria

   # URL de conexión a la base de datos (Ejemplo para PostgreSQL)
   # postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_db>
   DATABASE_URL=postgresql://vetlog_user:tu_contraseña_segura@localhost:5432/vetlog_db
   ```

   Para generar una clave secreta segura, puedes usar Python:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Carga las variables de entorno:**
   ```bash
   # En Linux/Mac:
   source .env
   # En Windows (PowerShell):
   Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
   ```

> ⚠️ **IMPORTANTE**: 
> - Nunca subas el archivo `.env` al control de versiones
> - Cada desarrollador debe crear su propio `.env` con sus propias claves
> - La aplicación no funcionará si no se configura la variable `SECRET_KEY`

## ✨ Notas adicionales

-   **Gestiona tus dependencias:** Si añades nuevas librerías, no olvides actualizar `requirements.txt`:
    ```bash
    pip freeze > requirements.txt
    ```
-   **Entorno de desarrollo:** Para optimizar el flujo de trabajo, puedes configurar la variable de entorno `FLASK_ENV`:
    ```bash
    # En Linux/Mac:
    export FLASK_ENV=development
    # En Windows:
    set FLASK_ENV=development
    ```

---

¡Gracias por usar nuestro proyecto! Si tienes alguna duda, no dudes en abrir un *issue*.
