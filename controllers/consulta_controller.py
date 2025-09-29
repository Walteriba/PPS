from flask import Blueprint, request, redirect, jsonify
from models.paciente import Paciente
from models.tutor import Tutor
from models.consulta import Consulta
from models import db
from datetime import datetime

#*******************************************************************#
# intento de hacer consulta_controller copiando paciente_controller #
#*******************************************************************#

consulta_bp = Blueprint("consulta_bp", __name__)    # Definición del Blueprint

# Endpoint para crear consulta (insert)
@consulta_bp.route("/consulta/nuevo", methods=["POST"])
def crear_consulta():
    nueva_consulta = Consulta(
        # La fecha aunque se puede modificar para cargar una consulta de días anteriores
        # por defecto toma la fecha actual
        fecha_actual=datetime.strptime(request.form["fecha"], "%Y-%m-%d"), 
        peso=float(request.form["peso"]), # Validar, no puede ser más de 100kg
        temperatura=float(request.form["temperatura"]), # Validar, no puede ser más de 50 grados
        anamnesis=request.form.get("anamnesis"),
        examen_fisico=request.form.get("examen_fisico"),
        diagnostico=request.form.get("diagnostico"),
        tratamiento=request.form.get("tratamiento"),
        # Validar que el paciente y tutor existan
        tutor_id=int(request.form["tutor_id"]),
        paciente_id=int(request.form["paciente_id"])
    )
    db.session.add(nueva_consulta)
    db.session.commit()
    return jsonify({"mensaje": "Consulta creada con éxito", "id": nueva_consulta.id}), 201   
                     
# Endpoint para actualizar una consulta
@consulta_bp.route("/consulta/<int:id>", methods=["PUT"])
def actualizar_consulta(id):
        # Buscar la consulta por ID
        consulta = Consulta.query.get(id)
        if not consulta:
            return jsonify({"error": "Consulta no encontrada"}), 404
        # Actualizar campos si vienen en el request.form
        # Usamos get con valor por defecto para no romper si falta el campo
        fecha = request.form.get("fecha")
        if fecha:
            consulta.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        peso = request.form.get("peso")
        if peso:
            consulta.peso = float(peso)
        temperatura = request.form.get("temperatura")
        if temperatura:
            consulta.temperatura = float(temperatura)
        consulta.anamnesis = request.form.get("anamnesis", consulta.anamnesis)
        consulta.examen_fisico = request.form.get("examen_fisico", consulta.examen_fisico)
        consulta.diagnostico = request.form.get("diagnostico", consulta.diagnostico)
        consulta.tratamiento = request.form.get("tratamiento", consulta.tratamiento)
        # Actualizar tutor y paciente si se envían sus IDs
        tutor_id = request.form.get("tutor_id")
        if tutor_id:
            tutor = Tutor.query.get(int(tutor_id))
            if not tutor:
                return jsonify({"error": "Tutor no encontrado"}), 400
            consulta.tutor = tutor
        paciente_id = request.form.get("paciente_id")
        if paciente_id:
            paciente = Paciente.query.get(int(paciente_id))
            if not paciente:
                return jsonify({"error": "Paciente no encontrado"}), 400
            consulta.paciente = paciente
        # Guardar cambios
        db.session.commit()
        return jsonify({"mensaje": "Consulta actualizada con éxito", "id": consulta.id}), 200

          
# Endpoint para eliminar una consulta
@consulta_bp.route("/consulta/<int:id>", methods=["DELETE"])
def eliminar_consulta(id):
        # Buscar consulta por ID
        consulta = Consulta.query.get(id)
        if not consulta:
            return jsonify({"error": "Consulta no encontrada"}), 404
        # Eliminar de la base de datos
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({"mensaje": "Consulta eliminada con éxito", "id": id}), 200

# Endpoint para obtener todas las consultas
@consulta_bp.route("/consultas", methods=["GET"])
def obtener_consultas():
    consultas = Consulta.query.all()
    resultado = []
    for consulta in consultas:
        resultado.append({
            "id": consulta.id,
            "fecha": consulta.fecha.strftime("%Y-%m-%d"),
            "peso": consulta.peso,
            "temperatura": consulta.temperatura,
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200

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
            "peso": consulta.peso,
            "temperatura": consulta.temperatura,
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200

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
            "peso": consulta.peso,
            "temperatura": consulta.temperatura,
            "anamnesis": consulta.anamnesis,
            "examen_fisico": consulta.examen_fisico,
            "diagnostico": consulta.diagnostico,
            "tratamiento": consulta.tratamiento,
            "tutor_id": consulta.tutor_id,
            "paciente_id": consulta.paciente_id
        })
    return jsonify(resultado), 200