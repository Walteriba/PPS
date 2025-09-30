# Puesta en marcha de un proyecto Flask

## Requisitos previos

- Python 3.x instalado
- pip instalado

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/Walteriba/PPS.git
    cd PPS
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate     # En Windows
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1. Exporta la variable de entorno FLASK_APP:
    ```bash
    export FLASK_APP=app.py      # En Linux/Mac
    set FLASK_APP=app.py         # En Windows
    ```

2. Ejecuta el servidor:
    ```bash
    flask run --debug
    ```

3. Accede a la aplicación en [http://localhost:5000](http://localhost:5000)

## Base de datos

1. Ejecuta el script de carga de datos de prueba (parado en la raíz del proyecto):
    ```bash
    python -m utils.cargar_db
    ```
     
## Notas

- Agrega tus dependencias a `requirements.txt`. => pip freeze > requirements.txt
- Para desarrollo, puedes usar `FLASK_ENV=development`.