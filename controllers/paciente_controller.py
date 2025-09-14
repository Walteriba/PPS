from flask import Blueprint, request, redirect, jsonify
from models.paciente import Paciente
from models.tutor import Tutor
from models import db
from datetime import datetime

# Definición del Blueprint
paciente_bp = Blueprint("paciente_bp", __name__)

# Endpoint para crear paciente (insert)
@paciente_bp.route("/paciente/nuevo", methods=["POST"])
def crear_paciente():
    try:
        nombre = request.form["nombre"]
        especie = request.form["especie"]
        raza = request.form["raza"]
        sexo = request.form["sexo"]
        color = request.form["color"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        tutor_id = request.form["tutor_id"]

        # Checkboxes -> booleanos
        activo = "activo" in request.form
        reproductor = "reproductor" in request.form
        castrado = "castrado" in request.form

        # Buscar tutor
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"error": "Tutor no encontrado"}), 400

        # Crear nuevo paciente
        nuevo_paciente = Paciente(
            nombre=nombre,
            especie=especie,
            raza=raza,
            sexo=sexo,
            color=color,
            fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d"),
            activo=activo,
            reproductor=reproductor,
            castrado=castrado,
            tutor=tutor
        )

        db.session.add(nuevo_paciente)
        db.session.commit()

        return jsonify({"mensaje": "Paciente creado con éxito", "id": nuevo_paciente.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
