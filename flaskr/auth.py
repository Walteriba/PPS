import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Registro
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Se requiere Usuario.'
        elif not password:
            error = 'Se requiere Password.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"El Usuario {username} ya esta registrado."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

'''
Esto es lo que hace la función de vista register:
1. @bp.route asocia la URL /register con la función de la vista register. Cuando Flask reciba
una petición a /auth/register, llamará a la vista register y utilizará el valor devuelto como
respuesta.
2. Si el usuario ha enviado el formulario, request.method será 'POST'. En este caso, empieza a
validar la entrada.
3. request.form es un tipo especial de dict que mapea las claves y valores del formulario
enviado. El usuario introducirá su nombre de usuario y su contraseña.
4. Valida que nombre de usuario y contraseña no estén vacíos.
5. Si la validación tiene éxito, inserte los nuevos datos del usuario en la base de datos.
db.execute toma una consulta SQL con marcadores de posición ? para cualquier entrada del
usuario, y una tupla de valores para reemplazar los marcadores de posición. La biblioteca de la
base de datos se encargará de escapar los valores para que no seas vulnerable a un ataque de
inyección SQL.
Por seguridad, las contraseñas nunca deben ser almacenadas en la base de datos directamente.
En su lugar, se utiliza generate_password_hash() para hacer un hash seguro de la
contraseña, y ese hash se almacena. Como esta consulta modifica los datos, es necesario
llamar después a db.commit() para guardar los cambios.
Se producirá un sqlite3.IntegrityError si el nombre de usuario ya existe, lo que
debería mostrarse al usuario como otro error de validación.
6. Después de almacenar al usuario, se le redirige a la página de inicio de sesión. url_for() genera
la URL para la vista de inicio de sesión basándose en su nombre. Esto es preferible a escribir la
URL directamente ya que permite cambiar la URL más tarde sin cambiar todo el código que enlaza
con ella. redirect() genera una respuesta de redirección a la URL generada.
7. Si la validación falla, se muestra el error al usuario. flash() almacena mensajes que pueden ser
recuperados al renderizar la plantilla.
8. Cuando el usuario navega inicialmente a auth/register, o hay un error de validación, se debe
mostrar una página HTML con el formulario de registro. render_template() renderizará una
plantilla que contiene el HTML
'''

# Inicio de sesión
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Usuario Incorrecto.'
        elif not check_password_hash(user['password'], password):
            error = 'Password Incorrecto.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

'''
1. El usuario se consulta primero y se almacena en una variable para su uso posterior.
fetchone() devuelve una fila de la consulta. Si la consulta no devuelve ningún resultado,
devuelve None. Más tarde, se utilizará fetchall(), que devuelve una lista de todos los
resultados.
2. check_password_hash() realiza el hash de la contraseña enviada de la misma forma que el
hash almacenado y los compara de forma segura. Si coinciden, la contraseña es válida.
3. session es una dict que almacena datos a través de las peticiones. Cuando la validación tiene
éxito, el id del usuario se almacena en una nueva sesión. Los datos se almacenan en
una cookie que se envía al navegador, y éste la devuelve con las siguientes peticiones.
Flask firma de forma segura los datos para que no puedan ser manipulados.
Ahora que el id del usuario está almacenado en el session, estará disponible en las siguientes
peticiones. Al principio de cada petición, si un usuario está conectado, su información debe ser cargada
and made available to other views.
'''

# antes de la solicitud de la aplicación
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

'''
bp.before_app_request() registra una función que se ejecuta antes de la función de vista, sin
importar la URL solicitada. load_logged_in_user comprueba si hay un id de usuario almacenado
en la session y obtiene los datos de ese usuario de la base de datos, almacenándolos en g.user, que
dura lo que dure la petición. Si no hay id de usuario, o si el id no existe, g.user será None.
'''

# Cierre de sesión
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

'''
Para cerrar la sesión, es necesario eliminar el id de usuario de la session.
Entonces load_logged_in_user no cargará un usuario en las siguientes peticiones.
'''

# Requerir autenticación en otras vistas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

'''
Este decorador devuelve una nueva función de vista que envuelve la vista original a la que se aplica. La
nueva función comprueba si hay un usuario cargado y redirige a la página de inicio de sesión en caso
contrario. Si se carga un usuario, se llama a la vista original y continúa normalmente.

Cuando se utiliza un blueprint, el nombre del blueprint se antepone al nombre de la función, por lo que
el endpoint de la función login que escribiste arriba es 'auth.login' porque lo agregaste al
blueprint 'auth'.
'''