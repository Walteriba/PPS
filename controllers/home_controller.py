from flask import Blueprint, render_template, request
from models.veterinaria import Veterinaria
from models.tutor import Tutor
from models.paciente import Paciente

# Definición del Blueprint
home_bp = Blueprint("home_bp", __name__)

# Home
@home_bp.route("/", methods=["GET"])
def home():
    pacientes = Paciente.query.all()
    return render_template("index.html", pacientes=pacientes)

# Busqueda de mascotas
@home_bp.route("/buscar", methods=["GET"])
def buscar_paciente():
    query = request.args.get("q")  # "q" será el name del input
    if not query:
        pacientes = Paciente.query.all()
    else:
        pacientes = Paciente.query.filter(Paciente.nombre.ilike(f"%{query}%")).all() # TODO: Mejorar búsqueda
    return render_template("index.html", pacientes=pacientes, search=query)

# Detalle de paciente
@home_bp.route("/paciente/<int:id>", methods=["GET"])
def detalle_paciente(id):
    paciente = Paciente.query.get(id)   
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return render_template("detalle_paciente.html", paciente=paciente, tutor=tutor)
    return "Mascota no encontrada", 404