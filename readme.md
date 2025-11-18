
# 👾 Puesta en marcha de Vetlog

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

## ⚙️ Configuración del entorno y modos de ejecución

En este proyecto existen dos formas de ejecutar la app:

- Modo desarrollo (debug) → con flask run

- Modo producción (release) → con Gunicorn (solo Linux)

> El proyecto usa Gunicorn como servidor WSGI para producción porque el servidor de producción esta en Linux.
> Existe otro servidor llamado Waitress, usado principalmente para Windows, pero no lo utilizamos, y no está en las dependencias del proyecto.

El proyecto utiliza variables del archivo `.env` para definir el modo de funcionamiento.

1. **Crea un archivo `.env` en la raíz del proyecto:**

   ```bash
    touch .env
   ```
   
2. **Añade las siguientes variables en el archivo `.env`:**

   ```bash
    FLASK_APP=app
    FLASK_ENV=production   # production / development
    DEBUG=False            # True para modo debug
    SECRET_KEY=            # Clave secreta para sesiones y seguridad (REQUERIDA)
    CLOUDINARY_CLOUD_NAME= # (REQUERIDA)
    CLOUDINARY_API_KEY=    # (REQUERIDA)
    CLOUDINARY_API_SECRET= # (REQUERIDA)
   ```
> Es necesario tener credenciales de [CLOUDINARY](https://cloudinary.com/) para este proyecto.

3. Para generar una clave secreta segura, puedes usar Python:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Carga las variables de entorno:**
   ```bash
   # En Linux/Mac:
   source .env
   # En Windows (PowerShell):
   Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
   ```

> ⚠️ **IMPORTANTE**: 
> - Nunca subas el archivo `.env` al control de versiones.
> - Cada desarrollador debe crear su propio `.env` con sus propias claves.
> - La aplicación no funcionará si no se configuran las variables.

### 🧪 MODO DESARROLLO (DEBUG)

1.  **Configura del `.env`:**
    ```bash
    FLASK_ENV=development
    DEBUG=True
    ```

2.  **Inicia el servidor de desarrollo:**
    ```bash
    flask run --debug
    ```
    El modo `--debug` reiniciará el servidor automáticamente con cada cambio.

3.  **¡Listo!** La app estará en: [http://localhost:5000](http://localhost:5000).

### 🚀 MODO PRODUCCIÓN (RELEASE)

Para producción, se usa Gunicorn, únicamente en Linux.

1.  **Configura del `.env`:**
    ```bash
    FLASK_ENV=production
    DEBUG=False
    ```

2.  **Ejecución en producción (solo Linux)**
    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
    ```
- `-w 4` → número de workers
- `app:app` → módulo + instancia Flask


## 🗃️ Base de datos

Este proyecto utiliza SQLite como motor de base de datos.

SQLite es liviano, no requiere instalación y almacena la información en un archivo local, ideal para aplicaciones pequeñas/medianas y despliegues simples.

1. Cuando arrancás la app (con `flask run` o con `gunicorn`), Flask SQLAlchemy ejecuta:

    ```bash
    db.create_all()
    ```

Esto garantiza que la base exista y todos los modelos estén creados.
No se necesita ejecutar migraciones para el estado inicial.

2. El archivo se encuentra en la raíz del proyecto:

    ```bash
    instance/vetlog.db
    ```

3. El proyecto incluye un script para cargar datos de prueba en la base de datos. Este script crea información básica útil para desarrollo.

    ```bash
    python -m utils.cargar_db
    ```

> Asegurate de tener el entorno virtual activado y de estar en la raíz del proyecto al ejecutarlo

## 📄 Logs del sistema

La aplicación genera logs tanto en consola como en archivos, dependiendo del modo de ejecución.

#### 🧪 En modo desarrollo (DEBUG=True)

- Los logs solo se muestran en consola.
- Se incluyen mensajes de nivel DEBUG.
- Útil para ver requests, respuestas y errores en tiempo real.

#### 🚀 En producción (DEBUG=False)

Los logs se guardan en la carpeta logs/ (se crea automáticamente en la raíz del proyecto).

- El archivo principal es:

    ```bash
    logs/vetlog.log
    ```

¿Qué queda registrado?

- Requests y responses (`before_request` / `after_request`)
- Errores no controlados
- Eventos importantes de inicio
- Acciones de autenticación

> No tenés que configurar nada extra, los logs cambian de comportamiento automáticamente según el valor de `DEBUG`en tu `.env`.

## ✨ Notas adicionales

-   **Gestiona tus dependencias:** Si añades nuevas librerías, no olvides actualizar `requirements.txt`:
    ```bash
    pip freeze > requirements.txt
    ```
---

¡Gracias por usar nuestro proyecto! Si tienes alguna duda, no dudes en abrir un *issue*.
