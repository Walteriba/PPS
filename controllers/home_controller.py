from flask import Blueprint, render_template, request
from models.tutor import Tutor
from models.paciente import Paciente
from dto.paciente_dto import PacienteDTO

# Definición del Blueprint
home_bp = Blueprint("home_bp", __name__)

# Home
@home_bp.route("/", methods=["GET"])
def home():
    # Obtener todos los pacientes y sus tutores, crear DTOs
    pacientes_dto = CreatePacienteDto(Tutor.query.all(), Paciente.query.all())
    return render_template("index.html", pacientes=pacientes_dto)

# Busqueda de mascotas
@home_bp.route("/buscar", methods=["GET"])
def buscar_paciente():
    # Obtener el parámetro de búsqueda desde la query string
    query_param = request.args.get("q")  # "q" será el name del input
    
    # Si no hay query, traer todos los pacientes, sino filtrar
    if not query_param:
        pacientes = Paciente.query.all()
        tutores = Tutor.query.all()
    else:
        pacientes = Paciente.query.filter(Paciente.nombre.ilike(f"%{query_param}%")).all() # TODO: Mejorar búsqueda
        tutores = Tutor.query.all() # TODO: Traer solo los tutores de los pacientes encontrados
        
    # Crear DTOs para los pacientes encontrados
    pacientes_dto = CreatePacienteDto(tutores, pacientes)
    return render_template("index.html", pacientes=pacientes_dto, search=query_param)

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
                tutor= f"{tutor.nombre} {tutor.apellido}"
            )
        )
    return pacientes_dto