from flask_login import login_required
from flask import Blueprint, render_template, request, jsonify, send_file
from models.paciente import Paciente
from models.tutor import Tutor
from models import db
from datetime import datetime
from utils.cloudinary_utils import subir_y_obtener_url
from models.consulta import Consulta
from utils.generar_reportes import crear_pdf_historia_clinica

paciente_bp = Blueprint("paciente_bp", __name__)


@paciente_bp.route("/paciente/<int:id>", methods=["GET"])
@login_required
def ver_paciente(id):
    # Obtener paciente y su tutor
    paciente = Paciente.query.get(id)
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return render_template(
            "paciente/detalle_paciente.html", paciente=paciente, tutor=tutor
        )
    # Si no se encuentra el paciente, mostrar un mensaje de error
    return "Mascota no encontrada", 404


@paciente_bp.route("/paciente/nuevo", methods=["GET"])
@login_required
def ver_nuevo_paciente():
    tutores = Tutor.query.all()
    tutor_id = request.args.get("tutor_id", type=int)
    return render_template(
        "paciente/nuevo_paciente.html", tutores=tutores, tutor_id=tutor_id
    )


@paciente_bp.route("/paciente/nuevo", methods=["POST"])
@login_required
def nuevo_paciente():
    # TODO: agregar validaciones faltantes
    # valida tutor_id primero
    tutor_id = request.form.get("tutor_id")
    if not tutor_id:
        return jsonify({"error": "tutor_id es requerido"}), 400
    try:
        tutor = Tutor.query.get(int(tutor_id))
    except ValueError:
        return jsonify({"error": "tutor_id debe ser un numero"}), 400
    if not tutor:
        return jsonify({"error": "Tutor no encontrado"}), 400

    # Procesar imagen si viene, sino usar default
    imagen = request.files.get("imagen")
    if imagen:
        url = subir_y_obtener_url(imagen)
    else:
        url = "/static/imgs/default-avatar.jpg"
    # Crear nuevo paciente con asignacion
    nuevo_paciente = Paciente(
        nombre=request.form["nombre"],
        especie=request.form["especie"],
        raza=request.form["raza"],
        sexo=request.form["sexo"],
        color=request.form["color"],
        fecha_nacimiento=datetime.strptime(
            request.form["fecha_nacimiento"], "%Y-%m-%d"
        ),
        imagen=url,
        reproductor=("reproductor" in request.form),
        castrado=("castrado" in request.form),
        tutor=tutor,
    )
    db.session.add(nuevo_paciente)
    db.session.commit()
    return (
        jsonify({"mensaje": "Paciente creado con éxito", "id": nuevo_paciente.id}),
        201,
    )


@paciente_bp.route("/paciente/actualizar/<int:id>", methods=["PUT"])
@login_required
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
    # Subir solo si se envía un archivo
    imagen = request.files.get("imagen")
    if imagen:
        paciente.imagen = subir_y_obtener_url(imagen)
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
    return (
        jsonify({"mensaje": "Paciente actualizado con éxito", "id": paciente.id}),
        200,
    )


@paciente_bp.route("/paciente/<int:paciente_id>/reporte", methods=["GET"])
@login_required
def generar_reporte_paciente(paciente_id):
    """
    Genera un reporte en PDF con toda la historia clínica de un paciente.
    """
    # 1. Obtener los datos de la base de datos.
    paciente = Paciente.query.get_or_404(paciente_id)
    tutor = paciente.tutor
    consultas = (
        Consulta.query.filter_by(paciente_id=paciente_id)
        .order_by(Consulta.fecha.asc())
        .all()
    )

    # 2. Llamar a la función de utilidad para que cree el PDF.
    pdf_buffer = crear_pdf_historia_clinica(paciente, tutor, consultas)

    # 3. Enviar el archivo PDF como respuesta.
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"reporte_{paciente.nombre.replace(' ', '_')}.pdf",
        mimetype="application/pdf",
    )
