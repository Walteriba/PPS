from flask import Blueprint, render_template, request
from sqlalchemy.orm import joinedload
from models.tutor import Tutor
from models.paciente import Paciente
from models.consulta import Consulta
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
    anamnesis = request.args.get("anamnesis", "").strip()
    diagnostico = request.args.get("diagnostico", "").strip()
    tratamiento = request.args.get("tratamiento", "").strip()
    nombre_tutor = request.args.get("nombre_tutor", "").strip()
    telefono = request.args.get("telefono", "").strip()
    direccion = request.args.get("direccion", "").strip()
    email = request.args.get("email", "").strip()

    # Consulta base
    base_query = Paciente.query

    if modo == "paciente":
        pacientes_query = base_query.join(Tutor)
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

    elif modo == "consulta":
        pacientes_query = base_query.join(Consulta).join(Tutor)
        if query:
            pacientes_query = pacientes_query.filter(Paciente.nombre.ilike(f"%{query}%"))
        if anamnesis:
            pacientes_query = pacientes_query.filter(Consulta.anamnesis.ilike(f"%{anamnesis}%"))
        if diagnostico:
            pacientes_query = pacientes_query.filter(Consulta.diagnostico.ilike(f"%{diagnostico}%"))
        if tratamiento:
            pacientes_query = pacientes_query.filter(Consulta.tratamiento.ilike(f"%{tratamiento}%"))

    elif modo == "tutor":
        pacientes_query = base_query.join(Tutor)
        if query:
            pacientes_query = pacientes_query.filter(Tutor.nombre.ilike(f"%{query}%"))
        if nombre_tutor:
            pacientes_query = pacientes_query.filter(Tutor.nombre.ilike(f"%{nombre_tutor}%"))
        if telefono:
            pacientes_query = pacientes_query.filter(Tutor.telefono.ilike(f"%{telefono}%"))
        if direccion:
            pacientes_query = pacientes_query.filter(Tutor.direccion.ilike(f"%{direccion}%"))
        if email:
            pacientes_query = pacientes_query.filter(Tutor.email.ilike(f"%{email}%"))

    pacientes = pacientes_query.options(joinedload(Paciente.tutor)).all()
    tutores = list({p.tutor for p in pacientes if p.tutor})

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
        "anamnesis": anamnesis,
        "diagnostico": diagnostico,
        "tratamiento": tratamiento,
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
                anamnesis,
                diagnostico,
                tratamiento,
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
    tutor_id = request.args.get("tutor_id", type=int)
    return render_template("nuevo_paciente.html", tutores=tutores, tutor_id=tutor_id)

# GET -> mostrar la vista editar_tutor.html
@home_bp.route("/tutor/<int:id>/editar", methods=["GET"])
def editar_tutor(id):
    tutor = Tutor.query.get_or_404(id)
    paciente = Paciente.query.filter_by(tutor_id=tutor.id).first()
    return render_template("editar_tutor.html", tutor=tutor, paciente=paciente)
