from flask import Blueprint, request, jsonify
from models.tutor import Tutor
from models import db

# Definición del Blueprint
tutor_bp = Blueprint("tutor_bp", __name__)

# Endpoint para crear tutor (insert)
@tutor_bp.route("/tutor/nuevo", methods=["POST"])
def crear_tutor():
    # Validación de campos obligatorios
    campos = ["nombre", "apellido", "telefono", "email", "direccion"]
    for campo in campos:
        if not request.form.get(campo):
            return jsonify({"error": f"{campo} es requerido"}), 400

    # Crear nuevo tutor
    nuevo_tutor = Tutor(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        telefono=request.form["telefono"],
        email=request.form["email"],
        direccion=request.form["direccion"]
    )

    db.session.add(nuevo_tutor)
    db.session.commit()

    return jsonify({"mensaje": "Tutor creado con éxito", "id": nuevo_tutor.id}), 201


# Endpoint para actualizar un tutor
@tutor_bp.route("/tutor/<int:id>", methods=["PUT"])
def actualizar_tutor(id):
    tutor = Tutor.query.get(id)
    if not tutor:
        return jsonify({"error": "Tutor no encontrado"}), 404

    # Actualizar solo si se envía el campo
    tutor.nombre = request.form.get("nombre", tutor.nombre)
    tutor.apellido = request.form.get("apellido", tutor.apellido)
    tutor.telefono = request.form.get("telefono", tutor.telefono)
    tutor.email = request.form.get("email", tutor.email)
    tutor.direccion = request.form.get("direccion", tutor.direccion)

    db.session.commit()

    return jsonify({"mensaje": "Tutor actualizado con éxito", "id": tutor.id}), 200
