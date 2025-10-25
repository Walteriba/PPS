#----------------------------------------------------
# Controlador para gestionar las consultas médicas
#----------------------------------------------------

from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from models.paciente import Paciente
from models.tutor import Tutor
from models.consulta import Consulta
from models import db
from utils.cloudinary_utils import subir_y_obtener_url
from models.archivo import Archivo

consulta_bp = Blueprint("consulta_bp", __name__)  # Definición del Blueprint

# Endpoint para crear consulta (insert)
@consulta_bp.route("/consulta/nuevo", methods=["POST"])
@login_required
def crear_consulta():
    """Crear una nueva consulta médica."""
    
    try:
        # Validaciones de datos y conversiones 
        fecha_consulta = datetime.strptime(request.form["fecha"], "%Y-%m-%d")
        tutor_id_consulta = int(request.form["tutor_id"])
        paciente_id_consulta = int(request.form["paciente_id"])

    except ValueError as e:
        # Manejo de errores de conversión
        return jsonify({"error": f"Error en el formato de datos. Verifique: fecha, tutor_id o paciente_id. Detalle: {e}"}), 400
    except KeyError as e:
        # Manejo de campos obligatorios faltantes
        return jsonify({"error": f"Campo obligatorio faltante: {e}"}), 400

    nueva_consulta = Consulta(
        fecha=fecha_consulta,
        
        # Campos de texto sin límite de caracteres
        peso=float(request.form["peso"]),  # Validar, no puede ser más de 100kg
        temperatura=float(request.form["temperatura"]),  # Validar, no puede ser más de 50 grados
        anamnesis=request.form.get("anamnesis"),
        examen_fisico=request.form.get("examen_fisico"),
        diagnostico=request.form.get("diagnostico"),
        tratamiento=request.form.get("tratamiento"),
        
        tutor_id=tutor_id_consulta,
        paciente_id=paciente_id_consulta
    )
    
    db.session.add(nueva_consulta)

    archivos = request.files.getlist("archivos")
    for archivo in archivos:
        if archivo and archivo.filename != "":
            url = subir_y_obtener_url(archivo)
            nuevo_archivo = Archivo(url=url)
            nueva_consulta.archivos.append(nuevo_archivo)

    db.session.commit()

    return (
        jsonify({"mensaje": "Consulta creada con éxito", "id": nueva_consulta.id}),
        201,
    )

# --------------------------------------------------------------------------------------

# Endpoint para actualizar una consulta 
@consulta_bp.route("/consulta/<int:id_consulta>", methods=["PUT"])
@login_required
def actualizar_consulta(id_consulta):
    consulta = Consulta.query.get(id_consulta)
    if not consulta:
        return jsonify({"error": "Consulta no encontrada"}), 404

    # --- Lógica de Actualización de Campos ---
    
    # 1. Fecha (Requiere conversión de string a datetime)
    fecha = request.form.get("fecha")
    peso = request.form.get("peso")
    if peso:
        consulta.peso = float(peso)
    if fecha is not None:
        try:
            consulta.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use AAAA-MM-DD"}), 400

    # 2. Anamnesis 
    anamnesis = request.form.get("anamnesis")
    if anamnesis is not None:
        consulta.anamnesis = anamnesis

    # 3. Examen Físico 
    examen_fisico = request.form.get("examen_fisico")
    if examen_fisico is not None:
        consulta.examen_fisico = examen_fisico

    # 4. Diagnóstico 
    diagnostico = request.form.get("diagnostico")
    if diagnostico is not None:
        consulta.diagnostico = diagnostico

    # 5. Tratamiento
    tratamiento = request.form.get("tratamiento")
    if tratamiento is not None:
        consulta.tratamiento = tratamiento
        

    # Lógica para AGREGAR nuevos archivos
    archivos = request.files.getlist("archivos")
    for archivo in archivos:
        if archivo.filename:
            url = subir_y_obtener_url(archivo)
            nuevo_archivo = Archivo(url=url)
            consulta.archivos.append(nuevo_archivo)

# Guardar cambios en la base de datos
    db.session.commit()

    return jsonify(
        {"mensaje": "Consulta actualizada exitosamente", "consulta_id": id_consulta}
    )

# Endpoint para ver una consulta específica
@consulta_bp.route("/consulta/<int:consulta_id>", methods=["GET"])
def ver_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    paciente = Paciente.query.get(consulta.paciente_id)
    tutor = Tutor.query.get(consulta.tutor_id)

    return render_template(
        "consulta.html", consulta=consulta, paciente=paciente, tutor=tutor
    )