from flask import Blueprint, render_template
from models.veterinaria import Veterinaria
from models.paciente import Paciente

# Datos de ejemplo (MOCK) - Deberían venir de una base de datos
veterinaria = Veterinaria("Veterinaria PPS")

mascotas = [
    Paciente(1, "Firulais", "Perro", 1),
    Paciente(2, "Michi", "Gato", 2),
    Paciente(3, "Nemo", "Pez", 1)
]

home_bp = Blueprint("home_bp", __name__)

# Home (maestro-detalle)
@home_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html", veterinaria=veterinaria, mascotas=mascotas)

# Detalle de mascota
@home_bp.route("/mascota/<int:id>", methods=["GET"])
def detalle_mascota(id):
    mascota = next((m for m in mascotas if m.id == id), None) # Método que busca la mascota por ID
    if mascota:
        return f"Aquí va el detalle de la mascota: {mascota.nombre}"
    return "Mascota no encontrada", 404