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
        # TODO: agregar validaciones faltantes
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
                     
# Endpoint para actualizar un paciente
@paciente_bp.route("/paciente/<int:id>", methods=["PUT"])
def actualizar_paciente(id):
        # Buscar el paciente por ID
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404
        # Actualizar campos si vienen en el request.form
        # Usamos get con valor por defecto para no romper si falta el campo
        paciente.nombre = request.form.get("nombre", paciente.nombre)
        paciente.especie = request.form.get("especie", paciente.especie)
        paciente.raza = request.form.get("raza", paciente.raza)
        paciente.sexo = request.form.get("sexo", paciente.sexo)
        paciente.color = request.form.get("color", paciente.color)
        # Fecha de nacimiento (convertir solo si se envía)
        fecha_nac = request.form.get("fecha_nacimiento")
        if fecha_nac:
            paciente.fecha_nacimiento = datetime.strptime(fecha_nac, "%Y-%m-%d")
        # Campos booleanos (checkboxes)
        paciente.activo = "activo" in request.form
        paciente.reproductor = "reproductor" in request.form
        paciente.castrado = "castrado" in request.form
        # Actualizar tutor si se envía tutor_id
        tutor_id = request.form.get("tutor_id")
        if tutor_id:
            tutor = Tutor.query.get(int(tutor_id))
            if not tutor:
                return jsonify({"error": "Tutor no encontrado"}), 400
            paciente.tutor = tutor
        # Guardar cambios
        db.session.commit()
        return jsonify({"mensaje": "Paciente actualizado con éxito", "id": paciente.id}), 200  