from flask import Blueprint, render_template
from models.veterinaria import Veterinaria
from models.paciente import Paciente

# Datos de ejemplo (MOCK) - Deberían venir de una base de datos
veterinaria = Veterinaria("Veterinaria PPS")

mascotas = [
    Paciente(1, "Firulais", "Perro", "Labrador", "Macho", "Marrón", "2020-05-10", True, False, True, 1),
    Paciente(2, "Michi", "Gato", "Siamés", "Hembra", "Blanco", "2021-03-15", True, False, False, 2),
    Paciente(3, "Nemo", "Pez", "Goldfish", "Macho", "Naranja", "2022-01-01", True, False, False, 1)
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