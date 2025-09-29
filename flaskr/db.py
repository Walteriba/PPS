import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

'''
g es un objeto especial que es único para cada solicitud. Se utiliza para almacenar datos a los que
podrían acceder varias funciones durante la petición. La conexión se almacena y se reutiliza en lugar de
crear una nueva conexión si se llama a get_db por segunda vez en la misma petición.
current_app es otro objeto especial que apunta a la aplicación Flask que maneja la solicitud. Como
has utilizado una fábrica de aplicaciones, no hay ningún objeto de aplicación cuando escribes el resto
de tu código. La llamada a get_db se realizará cuando la aplicación haya sido creada y esté
gestionando una petición, por lo que se puede utilizar current_app.
sqlite3.connect() establece una conexión con el fichero apuntado por la clave de
configuración DATABASE. Este archivo no tiene que existir todavía, y no lo hará hasta que se inicialice
la base de datos más tarde.
sqlite3.Row indica a la conexión que devuelva filas que se comporten como dicts. Esto permite
acceder a las columnas por su nombre.
close_db comprueba si se ha creado una conexión comprobando si se ha establecido g.db. Si la
conexión existe, se cierra. Más adelante le dirás a tu aplicación sobre la función close_db en la
fábrica de la aplicación para que sea llamada después de cada petición.
'''

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Borrar los datos existentes y crear nuevas tablas."""
    init_db()
    click.echo('Inicializó la base de datos.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

'''
open_resource() abre un archivo relativo al paquete flaskr, lo cual es útil ya que no
necesariamente se sabrá dónde está esa ubicación cuando se despliegue la aplicación
posteriormente. get_db devuelve una conexión a la base de datos, que se utiliza para ejecutar los
comandos leídos del archivo.
click.command() define un comando de línea de comandos llamado init-db que llama a la
función init_db y muestra un mensaje de éxito al usuario.
La llamada a sqlite3.register_converter() indica a Python cómo interpretar los valores de
fecha y hora de la base de datos. Convertimos el valor a un datetime.datetime.
'''

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

'''
app.teardown_appcontext() le dice a Flask que llame a esa función cuando se limpie después de
devolver la respuesta.
app.cli.add_command() añade un nuevo comando que puede ser llamado con el comando flask.
Importa y llama a esta función desde la fábrica. Coloca el nuevo código al final de la función de fábrica
antes de devolver la aplicación.
'''