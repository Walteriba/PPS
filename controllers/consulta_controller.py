#----------------------------------------------------
# Controlador para gestionar las consultas médicas
#----------------------------------------------------

from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from models.paciente import Paciente
from models.tutor import Tutor
from models.consulta import Consulta
from models import db

consulta_bp = Blueprint("consulta_bp", __name__)     

# Endpoint para crear consulta 
@consulta_bp.route("/consulta/nuevo", methods=["GET", "POST"])
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
        anamnesis=request.form.get("anamnesis"),
        examen_fisico=request.form.get("examen_fisico"),
        diagnostico=request.form.get("diagnostico"),
        tratamiento=request.form.get("tratamiento"),
        
        tutor_id=tutor_id_consulta,
        paciente_id=paciente_id_consulta
    )
    
    db.session.add(nueva_consulta)
    db.session.commit()
    return jsonify({"mensaje": "Consulta creada con éxito", "id": nueva_consulta.id}), 201

# --------------------------------------------------------------------------------------

# Endpoint para actualizar una consulta 
@consulta_bp.route("/consulta/<int:id_consulta>", methods=["PUT"])
def actualizar_consulta(id_consulta):
    # Buscar la consulta por ID
    consulta = Consulta.query.get(id_consulta)
    if not consulta:
        return jsonify({"error": "Consulta no encontrada"}), 404

    # --- Lógica de Actualización de Campos ---
    
    # 1. Fecha (Requiere conversión de string a datetime)
    fecha = request.form.get("fecha")
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
        
    # Guardar cambios en la base de datos
    db.session.commit()

    return jsonify({
        "mensaje": "Consulta actualizada exitosamente",
        "consulta_id": id_consulta
    })

# --------------------------------------------------------------------------------------

# Endpoint para eliminar una consulta
@consulta_bp.route("/consulta/<int:id_consulta>", methods=["DELETE"])
def eliminar_consulta(id_consulta):
    # Buscar consulta por ID
    consulta = Consulta.query.get(id_consulta)
    if not consulta:
        return jsonify({"error": "Consulta no encontrada"}), 404
    # Eliminar de la base de datos
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"mensaje": "Consulta eliminada con éxito", "id": id_consulta}), 200

# --------------------------------------------------------------------------------------

# Endpoint para obtener todas las consultas
@consulta_bp.route("/consultas", methods=["GET"])
def obtener_consultas():
    consultas = Consulta.query.all()
    resultado = []
    for consulta in consultas:
        resultado.append({
            "id": consulta.id,
            "fecha": consulta.fecha.strftime("%Y-%m-%d"),
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200

# --------------------------------------------------------------------------------------

# Endpoint para obtener una consulta por paciente
@consulta_bp.route("/consultas/paciente/<int:paciente_id>", methods=["GET"])
def obtener_consultas_por_paciente(paciente_id):
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).all()
    if not consultas:
        return jsonify({"error": "No se encontraron consultas para este paciente"}), 404
    resultado = []
    for consulta in consultas:
        resultado.append({
            "id": consulta.id,
            "fecha": consulta.fecha.strftime("%Y-%m-%d"),
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200

# --------------------------------------------------------------------------------------

# Endpoint para obtener una consulta por anamnesis
@consulta_bp.route("/consultas/anamnesis/<string:anamnesis>", methods=["GET"])
def obtener_consultas_por_anamnesis(anamnesis):
    consultas = Consulta.query.filter(Consulta.anamnesis.contains(anamnesis)).all()
    if not consultas:
        return jsonify({"error": "No se encontraron consultas con esta anamnesis"}), 404
    resultado = []
    for consulta in consultas:
        resultado.append({
            "id": consulta.id,
            "fecha": consulta.fecha.strftime("%Y-%m-%d"),
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200

# --------------------------------------------------------------------------------------

# Endpoint para ver una consulta específica (consulta.html existe ????)
@consulta_bp.route("/consulta/<int:consulta_id>", methods=["GET"])
def ver_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    paciente = Paciente.query.get(consulta.paciente_id)
    tutor = Tutor.query.get(consulta.tutor_id)
    
    return render_template(
        "consulta.html",
        consulta=consulta,
        paciente=paciente,
        tutor=tutor
    )