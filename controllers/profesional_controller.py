"""Controlador para gestionar los profesionales."""
from flask import Blueprint, request, jsonify
from models.profesional import Profesional
from models import db

# Definición del Blueprint
profesional_bp = Blueprint("profesional_bp", __name__)

# ----------------------------------------------------
# Endpoint para crear un profesional (POST)
# ----------------------------------------------------
@profesional_bp.route("/profesional/nuevo", methods=["POST"])
def crear_profesional():
    """Crea un nuevo profesional en la base de datos."""
    # Validación de campos obligatorios
    campos_obligatorios = ["nombre", "apellido", "matricula", "telefono", "email"]
    for campo in campos_obligatorios:
        if not request.form.get(campo):
            return jsonify({"error": f"El campo '{campo}' es requerido"}), 400

    # Crear una nueva instancia de Profesional
    nuevo_profesional = Profesional(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        matricula=request.form["matricula"],
        especialidad=request.form.get("especialidad"), # Opcional
        telefono=request.form["telefono"],
        email=request.form["email"],
    )

    db.session.add(nuevo_profesional)
    db.session.commit()

    return jsonify({"mensaje": "Profesional creado con éxito", "id": nuevo_profesional.id}), 201

# ----------------------------------------------------
# Endpoint para obtener un profesional por ID (GET)
# ----------------------------------------------------
@profesional_bp.route("/profesional/<int:id>", methods=["GET"])
def obtener_profesional(id):
    """Obtiene los datos de un profesional por su ID."""
    profesional = Profesional.query.get(id)
    if not profesional:
        return jsonify({"error": "Profesional no encontrado"}), 404

    return jsonify({
        "id": profesional.id,
        "nombre": profesional.nombre,
        "apellido": profesional.apellido,
        "matricula": profesional.matricula,
        "especialidad": profesional.especialidad,
        "telefono": profesional.telefono,
        "email": profesional.email
    }), 200

# ----------------------------------------------------
# Endpoint para actualizar un profesional (PUT)
# ----------------------------------------------------
@profesional_bp.route("/profesional/<int:id>", methods=["PUT"])
def actualizar_profesional(id):
    """Actualiza los datos de un profesional existente."""
    profesional = Profesional.query.get(id)
    if not profesional:
        return jsonify({"error": "Profesional no encontrado"}), 404

    # Actualizar campos usando .get() para permitir actualizaciones parciales
    profesional.nombre = request.form.get("nombre", profesional.nombre)
    profesional.apellido = request.form.get("apellido", profesional.apellido)
    profesional.matricula = request.form.get("matricula", profesional.matricula)
    profesional.especialidad = request.form.get("especialidad", profesional.especialidad)
    profesional.telefono = request.form.get("telefono", profesional.telefono)
    profesional.email = request.form.get("email", profesional.email)

    db.session.commit()

    return jsonify({"mensaje": "Profesional actualizado con éxito", "id": profesional.id}), 200
