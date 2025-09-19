from flask import Blueprint, render_template, request, redirect, url_for
from models.tutor import Tutor
from utils.db import db

# Blueprint para los tutores
tutor_bp = Blueprint("tutor_bp", __name__)

# ------------------------
# Crear nuevo tutor
# ------------------------
@tutor_bp.route("/tutor/nuevo", methods=["POST"])
def crear_tutor():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    direccion = request.form["direccion"]

    nuevo_tutor = Tutor(nombre=nombre, apellido=apellido, telefono=telefono, email=email, direccion=direccion)
    db.session.add(nuevo_tutor)
    db.session.commit()

    return redirect(url_for("tutor_bp.list_tutores")) #CAMBIAR LOS RETURN!!!!!

# ------------------------
# Actualizar tutor (guardar cambios)
# ------------------------
@tutor_bp.route("/tutor/actualizar/<id>", methods=["POST"])
def update_tutor(id):
    tutor = Tutor.query.get(id)

    tutor.nombre = request.form["nombre"]
    tutor.apellido = request.form["apellido"]
    tutor.telefono = request.form["telefono"]
    tutor.email = request.form["email"]

    db.session.commit()
    return redirect(url_for("tutor_bp.list_tutores"))
