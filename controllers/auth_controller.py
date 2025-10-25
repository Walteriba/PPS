from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models.usuario import Usuario
from models import db

# Definición del Blueprint
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Maneja el inicio de sesión de usuarios."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Login exitoso
            login_user(user)
            # Redirigir a la página que intentaba acceder o al home
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home_bp.buscar"))
        
        # Login fallido
        flash("Email o contraseña incorrectos")
        return redirect(url_for("auth_bp.login"))
    
    # GET: mostrar formulario de login
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Maneja el registro de nuevos usuarios."""
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Verificar si el email ya está registrado
        if Usuario.query.filter_by(email=email).first():
            flash("El email ya está registrado")
            return redirect(url_for("auth_bp.register"))
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Login automático después del registro
        login_user(nuevo_usuario)
        return redirect(url_for("home_bp.buscar"))
    
    # GET: mostrar formulario de registro
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    """Cierra la sesión del usuario."""
    logout_user()
    return redirect(url_for("auth_bp.login"))