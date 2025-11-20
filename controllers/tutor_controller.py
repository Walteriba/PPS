from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from models import db
from models.paciente import Paciente
from models.tutor import Tutor
from sqlalchemy.exc import IntegrityError 

tutor_bp = Blueprint("tutor_bp", __name__)


@tutor_bp.route("/tutor/nuevo", methods=["GET"])
@login_required
def ver_nuevo_tutor():
    return render_template("tutor/nuevo_tutor.html")


@tutor_bp.route("/tutor/<int:id>/editar", methods=["GET"])
@login_required
def ver_actualizar_tutor(id):
    tutor = Tutor.query.get_or_404(id)
    paciente = Paciente.query.filter_by(tutor_id=tutor.id).first()
    return render_template("tutor/editar_tutor.html", tutor=tutor, paciente=paciente)


@tutor_bp.route("/tutor/nuevo", methods=["POST"])
@login_required
def nuevo_tutor():
    # Validación de campos obligatorios
    campos = ["nombre", "apellido", "telefono", "email", "direccion"]
    for campo in campos:
        if not request.form.get(campo):
            return jsonify({"error": f"{campo} es requerido"}), 400

    email_tutor = request.form["email"]
    
    # 1. VERIFICACIÓN DE RESTRICCIÓN ÚNICA (EMAIL)
    if Tutor.query.filter_by(email=email_tutor).first():
        return jsonify({"error": "Ya existe un tutor registrado con este email."}), 400

    # Crear nuevo tutor
    nuevo_tutor = Tutor(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        telefono=request.form["telefono"],
        email=email_tutor,
        direccion=request.form["direccion"],
    )

    db.session.add(nuevo_tutor)

    # Manejo de errores de la Base de Datos (IntegrityError)
    # Envuelve el commit en un try/except para capturar fallos de concurrencia
    try:
        db.session.commit()
    except IntegrityError:
        # Si falla el commit por unicidad, deshace la operación y devuelve un 400.
        db.session.rollback()
        return jsonify({"error": "Ya existe un tutor registrado con este email."}), 400

    # Retorno de éxito, código 201 (Creado)
    return jsonify({"mensaje": "Tutor creado con éxito", "id": nuevo_tutor.id}), 201


@tutor_bp.route("/tutor/<int:id>", methods=["PUT"])
@login_required
def actualizar_tutor(id):
    # Buscar el tutor por ID [2]
    tutor = Tutor.query.get(id)
    if not tutor:
        return jsonify({"error": "Tutor no encontrado"}), 404

    # Actualizar solo si se envía el campo, usando get con valor por defecto [5]
    tutor.nombre = request.form.get("nombre", tutor.nombre)
    tutor.apellido = request.form.get("apellido", tutor.apellido)
    tutor.telefono = request.form.get("telefono", tutor.telefono)
    tutor.email = request.form.get("email", tutor.email)
    tutor.direccion = request.form.get("direccion", tutor.direccion)

    # Nota: También deberías añadir aquí el manejo de IntegrityError para el commit
    # si el email se actualiza a uno ya existente.
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ya existe un tutor registrado con este email."}), 400

    # Retorno de éxito, código 200 (OK) [3]
    return jsonify({"mensaje": "Tutor actualizado con éxito", "id": tutor.id}), 200