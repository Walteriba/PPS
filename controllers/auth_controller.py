from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario
from models import db

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_bp.login_page"))
    return redirect(url_for("search_bp.buscar"))


@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Muestra el formulario de inicio de sesión."""
    return render_template("auth/login.html")


@auth_bp.route("/login", methods=["POST"])
def login_submit():
    """Procesa el inicio de sesión de usuarios."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = Usuario.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # Login exitoso
        login_user(user)
        # Redirigir a la página que intentaba acceder o al home
        next_page = request.args.get("next")
        return redirect(next_page or url_for("search_bp.buscar"))

    # Login fallido
    flash("Email o contraseña incorrectos")
    return redirect(url_for("auth_bp.login_page"))


@auth_bp.route("/register", methods=["GET"])
def register_page():
    """Muestra el formulario de registro."""
    return render_template("auth/register.html")


@auth_bp.route("/register", methods=["POST"])
def register_submit():
    """Procesa el registro de nuevos usuarios."""
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    password = request.form.get("password")

    # Verificar si el email ya está registrado
    if Usuario.query.filter_by(email=email).first():
        flash("El email ya está registrado")
        return redirect(url_for("auth_bp.register_page"))

    # Crear nuevo usuario
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    nuevo_usuario.set_password(password)

    db.session.add(nuevo_usuario)
    db.session.commit()

    # Login automático después del registro
    login_user(nuevo_usuario)
    return redirect(url_for("search_bp.buscar"))


@auth_bp.route("/logout")
@login_required
def logout():
    """Cierra la sesión del usuario."""
    logout_user()
    return redirect(url_for("auth_bp.login_page"))
