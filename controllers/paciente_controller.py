from flask import Blueprint, request, jsonify
from models.paciente import Paciente
from models.tutor import Tutor
from models.imagen import Imagen
from models import db
from datetime import datetime
from utils.cloudinary_utils import subir_y_obtener_url

# Definición del Blueprint
paciente_bp = Blueprint("paciente_bp", __name__)

# Endpoint para agregar imágenes adicionales a un paciente
@paciente_bp.route("/paciente/<int:id>/imagen", methods=["POST"])
def agregar_imagen_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404
    archivos = request.files.getlist("imagen")
    urls_nuevas = []
    for archivo in archivos:
        if archivo and archivo.filename != "":
            url = subir_y_obtener_url(archivo)
            nueva_imagen = Imagen(url=url, paciente_id=paciente.id)
            db.session.add(nueva_imagen)
            urls_nuevas.append(url)
    db.session.commit()
    return jsonify({"mensaje": "Imágenes agregadas", "urls": urls_nuevas}), 201

# Endpoint para consultar todas las imágenes de un paciente
@paciente_bp.route("/paciente/<int:id>/imagenes", methods=["GET"])
def obtener_imagenes_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"error": "Paciente no encontrado"}), 404
    imagenes = Imagen.query.filter_by(paciente_id=id).all()
    urls = [img.url for img in imagenes]
    return jsonify({"imagenes": urls}), 200

# Métodos auxiliares
def validar_imagen(imagen):
    if imagen:
        url = subir_y_obtener_url(imagen)
    else:
        url = "/static/imgs/default-avatar.jpg"
    return url 

# Endpoint para crear paciente (insert)
@paciente_bp.route("/paciente/nuevo", methods=["POST"])
def crear_paciente():
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
    # TODO: agregar validaciones faltantes
    # valida tutor_id primero 
    tutor_id = request.form.get("tutor_id")
    if not tutor_id: 
        return jsonify({"error": "tutor_id es requerido"}), 400
    try: 
        tutor = Tutor.query.get(int(tutor_id))
    except ValueError:  
        return jsonify({"error": "tutor_id debe ser un numero"}),400
    if not tutor: 
        return jsonify({"error": "Tutor no encontrado"}), 400   
    
    # Procesar imagen si viene, sino usar default
    imagen = request.files.get("imagen")
    url = validar_imagen(imagen)
    if imagen:
        url = subir_y_obtener_url(imagen)
    else:
        url = "/static/imgs/default-avatar.jpg"
           
    # Crear nuevo paciente con asignacion 
>>>>>>> ec869bb (Refactor: separar lógica de imágenes adicionales y limpiar actualización de paciente)
    nuevo_paciente = Paciente(
        nombre=request.form["nombre"],
        especie=request.form["especie"],
        raza=request.form["raza"],
        sexo=request.form["sexo"],
        color=request.form["color"],
<<<<<<< HEAD
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


=======
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
       
       # Procesar imagen si viene, sino usar default
        imagen = request.files.get("imagen")
        url = validar_imagen(imagen)
        
        # Crear nuevo paciente con asignacion 
        nuevo_paciente = Paciente(
            nombre=request.form["nombre"],
            especie=request.form["especie"],
            raza=request.form["raza"],
            sexo=request.form["sexo"],
            color=request.form["color"],
            fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d"),
            imagen=url,
            activo=("activo" in request.form),
            reproductor=("reproductor" in request.form),
            castrado=("castrado" in request.form),
            tutor=tutor
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        return jsonify({"mensaje": "Paciente creado con éxito", "id": nuevo_paciente.id}), 201   
=======
        fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d"),
        imagen=url,
        activo=("activo" in request.form),
        reproductor=("reproductor" in request.form),
        castrado=("castrado" in request.form),
        tutor=tutor
    )
    db.session.add(nuevo_paciente)
    db.session.commit()
    return jsonify({"mensaje": "Paciente creado con éxito", "id": nuevo_paciente.id}), 201   
>>>>>>> ec869bb (Refactor: separar lógica de imágenes adicionales y limpiar actualización de paciente)
                     
>>>>>>> e9c74f2 (logica paciente)
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

    # TODO: Imagen (subir solo si se envía un archivo)
    imagen = request.files.get("imagen")
    eliminar_imagen = "eliminar_imagen" in request.form

    if eliminar_imagen:
        paciente.imagen = "/static/imgs/default-avatar.jpg"
    elif imagen:
        paciente.imagen = validar_imagen(imagen)
    # Si no se marca eliminar ni se sube imagen, se conserva la actual

    # Campos booleanos (checkboxes)
    paciente.activo = "activo" in request.form
    paciente.reproductor = "reproductor" in request.form
    paciente.castrado = "castrado" in request.form

    # Guardar todo
    db.session.commit()

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