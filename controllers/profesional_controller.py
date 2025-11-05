from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models.profesional import Profesional
from models import db

profesional_bp = Blueprint("profesional_bp", __name__)


@profesional_bp.route("/profesionales", methods=["GET"])
@login_required
def ver_profesionales():
    profesionales = Profesional.query.all()
    return render_template(
        "profesional/profesionales.html", profesionales=profesionales
    )


@profesional_bp.route("/profesional/nuevo", methods=["GET"])
@login_required
def ver_nuevo_profesional():
    return render_template("profesional/alta_profesional.html")


@profesional_bp.route("/profesional/editar/<int:id>", methods=["GET"])
@login_required
def ver_actualizar_profesional(id):
    profesional = Profesional.query.get_or_404(id)
    return render_template(
        "profesional/editar_profesional.html", profesional=profesional
    )


@profesional_bp.route("/profesional/nuevo", methods=["POST"])
@login_required
def nuevo_profesional():
    # Validación de campos obligatorios
    campos_obligatorios = ["nombre", "apellido"]
    for campo in campos_obligatorios:
        if not request.form.get(campo):
            return jsonify({"error": f"El campo '{campo}' es requerido"}), 400

    # Crear una nueva instancia de Profesional
    nuevo_profesional = Profesional(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        matricula=request.form.get("matricula"),
        especialidad=request.form.get("especialidad"),
        telefono=request.form.get("telefono"),
        email=request.form.get("email"),
    )

    db.session.add(nuevo_profesional)
    db.session.commit()

    return (
        jsonify(
            {"mensaje": "Profesional creado con éxito", "id": nuevo_profesional.id}
        ),
        201,
    )


@profesional_bp.route("/profesional/<int:id>", methods=["PUT"])
@login_required
def actualizar_profesional(id):
    profesional = Profesional.query.get(id)
    if not profesional:
        return jsonify({"error": "Profesional no encontrado"}), 404

    # Actualizar campos usando .get() para permitir actualizaciones parciales
    profesional.nombre = request.form.get("nombre", profesional.nombre)
    profesional.apellido = request.form.get("apellido", profesional.apellido)
    profesional.matricula = request.form.get("matricula", profesional.matricula)
    profesional.especialidad = request.form.get(
        "especialidad", profesional.especialidad
    )
    profesional.telefono = request.form.get("telefono", profesional.telefono)
    profesional.email = request.form.get("email", profesional.email)

    db.session.commit()

    return (
        jsonify({"mensaje": "Profesional actualizado con éxito", "id": profesional.id}),
        200,
    )
