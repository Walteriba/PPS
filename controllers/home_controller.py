from flask import Blueprint, render_template, request
from models.tutor import Tutor
from models.paciente import Paciente
from dto.paciente_dto import PacienteDTO

# Definición del Blueprint
home_bp = Blueprint("home_bp", __name__)

# Métodos Auxiliares
def CreatePacienteDto(tutores, pacientes):
    pacientes_dto = []
    # Recorremos los pacientes y buscamos su tutor correspondiente y creamos el DTO
    for paciente in pacientes:
        tutor = next(t for t in tutores if t.id == paciente.tutor_id)
        pacientes_dto.append(
            PacienteDTO(
                id=paciente.id,
                imagen=paciente.imagen,
                nombre=paciente.nombre,
                especie=paciente.especie,
                raza=paciente.raza,
                tutor=f"{tutor.nombre} {tutor.apellido}",
            )
        )
    return pacientes_dto

# Home
@home_bp.route("/", methods=["GET"])
# Busqueda de pacientes y tutores
@home_bp.route("/buscar", methods=["GET"])
def buscar():
    # Parámetros de búsqueda
    query = request.args.get("q", "").strip()
    modo = request.args.get("modo", "paciente")
    especie = request.args.get("especie", "").strip()
    raza = request.args.get("raza", "").strip()
    color = request.args.get("color", "").strip()
    reproductor = request.args.get("reproductor") == "1"
    castrado = request.args.get("castrado") == "1"
    nombre_tutor = request.args.get("nombre_tutor", "").strip()
    telefono = request.args.get("telefono", "").strip()
    direccion = request.args.get("direccion", "").strip()
    email = request.args.get("email", "").strip()
    # Consultas base
    pacientes_query = Paciente.query
    tutores_query = Tutor.query

    if modo == "paciente":
        if query:
            pacientes_query = pacientes_query.filter(Paciente.nombre.ilike(f"%{query}%"))
        if especie:
            pacientes_query = pacientes_query.filter(Paciente.especie.ilike(f"%{especie}%"))
        if raza:
            pacientes_query = pacientes_query.filter(Paciente.raza.ilike(f"%{raza}%"))
        if color:
            pacientes_query = pacientes_query.filter(Paciente.color.ilike(f"%{color}%"))
        if reproductor:
            pacientes_query = pacientes_query.filter(Paciente.reproductor.is_(True))
        if castrado:
            pacientes_query = pacientes_query.filter(Paciente.castrado.is_(True))

        pacientes = pacientes_query.all()

        # Solo traer tutores de los pacientes encontrados
        tutores_ids = {p.tutor_id for p in pacientes}
        tutores = Tutor.query.filter(Tutor.id.in_(tutores_ids)).all()

    else:
        if query:
            tutores_query = tutores_query.filter(Tutor.nombre.ilike(f"%{query}%"))
        if nombre_tutor:
            tutores_query = tutores_query.filter(Tutor.nombre.ilike(f"%{nombre_tutor}%"))
        if telefono:
            tutores_query = tutores_query.filter(Tutor.telefono.ilike(f"%{telefono}%"))
        if direccion:
            tutores_query = tutores_query.filter(Tutor.direccion.ilike(f"%{direccion}%"))
        if email:
            tutores_query = tutores_query.filter(Tutor.email.ilike(f"%{email}%"))

        tutores = tutores_query.all()

        # Solo traer pacientes de los tutores encontrados
        pacientes = Paciente.query.filter(Paciente.tutor_id.in_([t.id for t in tutores])).all()

    # DTO
    pacientes_dto = CreatePacienteDto(tutores, pacientes)
    
    # Parámetros de búsqueda para mantener en el formulario
    search = {
        "query": query,
        "modo": modo,
        "especie": especie,
        "raza": raza,
        "color": color,
        "reproductor": bool(reproductor),
        "castrado": bool(castrado),
        "nombre_tutor": nombre_tutor,
        "telefono": telefono,
        "direccion": direccion,
        "email": email,
        # Saber si hay filtros avanzados activos para mantener el desplegable abierto
        "advanced": any(
            [
                especie,
                raza,
                color,
                reproductor,
                castrado,
                nombre_tutor,
                telefono,
                direccion,
                email,
            ]
        ),
    }

    return render_template("index.html", pacientes=pacientes_dto, search=search)


# Detalle de paciente
@home_bp.route("/paciente/<int:id>", methods=["GET"])
def detalle_paciente(id):
    # Obtener paciente y su tutor
    paciente = Paciente.query.get(id)
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return render_template("detalle_paciente.html", paciente=paciente, tutor=tutor)
    # Si no se encuentra el paciente, mostrar un mensaje de error
    return "Mascota no encontrada", 404


# TODO (Backend): Endpoints temporales creados para probar el frontend.
# GET -> mostrar la vista nuevo_tutor.html
@home_bp.route("/tutor/nuevo", methods=["GET"])
def nuevo_tutor():
    return render_template("nuevo_tutor.html")


# GET -> mostrar la vista nuevo_paciente.html
@home_bp.route("/paciente/nuevo", methods=["GET"])
def nuevo_paciente():
    tutores = Tutor.query.all()
    return render_template("nuevo_paciente.html", tutores=tutores)
