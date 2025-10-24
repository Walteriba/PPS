from flask import Blueprint, request, jsonify, send_file, current_app
from models.paciente import Paciente
from models.tutor import Tutor
from models import db
from datetime import datetime
from utils.cloudinary_utils import subir_y_obtener_url
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from models.consulta import Consulta
import os

# Definición del Blueprint
paciente_bp = Blueprint("paciente_bp", __name__)


# Endpoint para crear paciente (insert)
@paciente_bp.route("/paciente/nuevo", methods=["POST"])
def crear_paciente():
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


# Endpoint para actualizar un paciente
@paciente_bp.route("/paciente/actualizar/<int:id>", methods=["PUT"])
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

# --- Endpoint para Generar Reporte ---
@paciente_bp.route("/paciente/<int:paciente_id>/reporte", methods=["GET"])
def generar_reporte_paciente(paciente_id):
    """
    Genera un reporte en PDF con toda la historia clínica de un paciente.
    """
    # 1. Validar que el paciente exista y obtener sus datos.
    paciente = Paciente.query.get_or_404(paciente_id)
    tutor = paciente.tutor # Acceder al tutor a través de la relación

    # 2. Obtener todas las consultas del paciente.
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).order_by(Consulta.fecha.asc()).all()

    # 3. Crear el PDF en memoria.
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50  # Posición Y inicial.

    # --- Cabecera del PDF ---
    # Título
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, f"Historia Clínica: {paciente.nombre}")
    y -= 30

    # Lógica para la imagen del paciente
    imagen_path = paciente.imagen
    try:
        if imagen_path.startswith('http'): # Si es una URL de Cloudinary
            response = requests.get(imagen_path, stream=True)
            response.raise_for_status()
            p.drawImage(BytesIO(response.content), width - 150, y - 60, width=100, height=100, preserveAspectRatio=True, mask='auto')
        else: # Si es una ruta local (imagen por defecto)
            # Construye la ruta absoluta al archivo estático
            full_path = os.path.join(current_app.root_path, imagen_path.strip('/'))
            if os.path.exists(full_path):
                p.drawImage(full_path, width - 150, y - 60, width=100, height=100, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Error al cargar la imagen: {e}") # Opcional: loguear el error

    # Datos del Paciente
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Datos del Paciente")
    p.setFont("Helvetica", 10)
    y -= 15
    p.drawString(55, y, f"Especie: {paciente.especie} | Raza: {paciente.raza} | Sexo: {paciente.sexo}")
    y -= 15
    p.drawString(55, y, f"Fecha de Nacimiento: {paciente.fecha_nacimiento.strftime('%d/%m/%Y')}")
    y -= 25

    # Datos del Tutor
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Datos del Tutor")
    p.setFont("Helvetica", 10)
    y -= 15
    p.drawString(55, y, f"Nombre: {tutor.nombre} {tutor.apellido}")
    y -= 15
    p.drawString(55, y, f"Teléfono: {tutor.telefono}")
    y -= 25

    # Línea separadora
    p.line(50, y, width - 50, y)
    y -= 20

    # --- Contenido de cada consulta ---
    if not consultas:
        p.drawString(50, y, "No se encontraron consultas para este paciente.")
    else:
        for consulta in consultas:
            if y < 120:  # Si queda poco espacio, crea una nueva página.
                p.showPage()
                y = height - 70

            p.setFont("Helvetica-Bold", 12)
            p.drawString(60, y, f"Fecha: {consulta.fecha.strftime('%d/%m/%Y')}")
            y -= 20
            
            p.setFont("Helvetica", 10)
            p.drawString(70, y, f"Anamnesis: {consulta.anamnesis or 'N/A'}")
            y -= 15
            p.drawString(70, y, f"Diagnóstico: {consulta.diagnostico or 'N/A'}")
            y -= 15
            p.drawString(70, y, f"Tratamiento: {consulta.tratamiento or 'N/A'}")
            y -= 25 # Espacio extra para la siguiente consulta.

    # 4. Guardar y devolver el archivo PDF.
    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"reporte_{paciente.nombre.replace(' ', '_')}.pdf",
        mimetype="application/pdf"
    )
    