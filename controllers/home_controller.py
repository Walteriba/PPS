from flask import Blueprint, render_template
from models.veterinaria import Veterinaria
from models.tutor import Tutor
from models.paciente import Paciente

veterinaria = Veterinaria("Veterinaria PPS") # TODO: Implementar modelo

# Definición del Blueprint
home_bp = Blueprint("home_bp", __name__)

# Home
@home_bp.route("/", methods=["GET"])
def home():
    pacientes = Paciente.query.all()
    return render_template("index.html", veterinaria=veterinaria, pacientes=pacientes)

# Detalle de mascota
@home_bp.route("/paciente/<int:id>", methods=["GET"])
def detalle_paciente(id):
    paciente = Paciente.query.get(id)   
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return render_template("detalle_mascota.html", paciente=paciente, tutor=tutor, veterinaria=veterinaria)
    return "Mascota no encontrada", 404