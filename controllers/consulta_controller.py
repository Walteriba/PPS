"""Controlador para gestionar las consultas médicas."""
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from models.paciente import Paciente
from models.tutor import Tutor
from models.consulta import Consulta
from models import db
from utils.cloudinary_utils import subir_y_obtener_url
from models.archivo import Archivo

consulta_bp = Blueprint("consulta_bp", __name__)    # Definición del Blueprint

# Endpoint para crear consulta (insert)
@consulta_bp.route("/consulta/nuevo", methods=["GET", "POST"])
def crear_consulta():
    data = request.form
    archivo = request.files.getlist("archivo")
    """Crear una nueva consulta médica."""
    try:
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
    
    archivo_subido = request.files.getlist("archivo")
    for archivo in archivo_subido:
        url = subir_y_obtener_url(archivo)
        nuevo_archivo = Archivo(
            url=url,
            paciente_id=nueva_consulta.paciente_id,
            consulta_id=nueva_consulta.id,
        )
            nueva_consulta.archivos.append(nuevo_archivo)

        db.session.add(nuevo_archivo)
    db.session.commit()

    return jsonify({"mensaje": "Consulta creada con éxito", "id": nueva_consulta.id}), 201

# Endpoint para actualizar una consulta
@consulta_bp.route("/consulta/<int:id_consulta>", methods=["PUT"])
def actualizar_consulta(id_consulta):
    try:
        consulta = Consulta.query.get(id_consulta)
        if not consulta:
            return jsonify({"error": "Consulta no encontrada"}), 404

    # Actualizar campos si vienen en el request.form
    fecha = request.form.get("fecha")
    if fecha:
        consulta.fecha = datetime.strptime(fecha, "%Y-%m-%d")

    peso = request.form.get("peso")
    if peso:
        consulta.peso = float(peso)
     # Lógica para ELIMINAR archivos existentes
        ids_a_eliminar = request.form.getlist("archivos_a_eliminar")
        if ids_a_eliminar:
            # Filtramos los archivos que pertenecen a la consulta y cuyo ID está en la lista a eliminar
            archivos_para_borrar = [archivo for archivo in consulta.archivos if str(archivo.id) in ids_a_eliminar]
            for archivo in archivos_para_borrar:
                # Simplemente lo removemos de la sesión y el 'delete-orphan' se encarga del resto
                db.session.delete(archivo)

        # Lógica para AGREGAR nuevos archivos
        archivos_nuevos = request.files.getlist("archivos_nuevos")
        for archivo in archivos_nuevos:
            if archivo.filename:
                url = subir_y_obtener_url(archivo)
                nuevo_archivo = Archivo(
                    url=url,
                    paciente_id=consulta.paciente_id,
                    consulta_id=consulta.id
                )
                db.session.add(nuevo_archivo)
        
        return jsonify({
            "mensaje": "Consulta actualizada exitosamente",
            "consulta_id": id_consulta
        })
    # Guardar cambios en la base de datos
    db.session.commit()

    return jsonify({
        "mensaje": "Consulta actualizada exitosamente",
        "consulta_id": id_consulta
    })

# Endpoint para eliminar una consulta
@consulta_bp.route("/consulta/<int:id>", methods=["DELETE"])
def eliminar_consulta(id_consulta):
    # Buscar consulta por ID
    consulta = Consulta.query.get(id_consulta)
    if not consulta:
        return jsonify({"error": "Consulta no encontrada"}), 404
    # Eliminar de la base de datos
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"mensaje": "Consulta eliminada con éxito", "id": id_consulta}), 200

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
            "paciente_id": consulta.paciente_id,
            "archivo": [archivo.url for archivo in consulta.archivos]
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
            "paciente_id": consulta.paciente_id,
            "archivo": [archivo.url for archivo in consulta.archivos]
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
            "paciente_id": consulta.paciente_id,
            "archivo": [archivo.url for archivo in consulta.archivos]
        })
    return jsonify(resultado), 200

# Endpoint para ver una consulta específica
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