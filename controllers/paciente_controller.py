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
        #valida tutor_id primero 
        tutor_id = request.form.get("tutor_id")
        if not tutor_id: 
            return jsonify({"error": "tutor_id es requerido"}), 400

        try: 
            tutor = Tutor.query.get(int(tutor_id))
        except ValueError:  
            return jsonify({"error": "tutor_id debe ser un numero"}),400

        if not tutor: 
            return jsonify({"error": "Tutor no encontrado"}), 400   


        # Crear nuevo paciente con asignacion 
        nuevo_paciente = Paciente(
            nombre=request.form["nombre"],
            especie=request.form["especie"],
            raza=request.form["raza"],
            sexo=request.form["sexo"],
            color=request.form["color"],
            fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d"),
            activo=("activo" in request.form),
            reproductor=("reproductor" in request.form),
            castrado=("castrado" in request.form),
            tutor=tutor
        )

        db.session.add(nuevo_paciente)
        db.session.commit()

        return jsonify({"mensaje": "Paciente creado con éxito", "id": nuevo_paciente.id}), 201
    except Exception as e: #captura los posibles errores tanto de la falta de campo como de formato 
        db.session.rollback()
        mensaje = str(e)
        if isinstance(e, KeyError):
            mensaje = f"Falta el campo: {e.args[0]}"
        elif isinstance(e, ValueError):
            mensaje = f"Formato inválido: {str(e)}"
        return jsonify({"error": mensaje}), 400

