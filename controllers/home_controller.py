from flask import Blueprint, render_template
from models.veterinaria import Veterinaria
from models.tutor import Tutor
from models.paciente import Paciente

<<<<<<< HEAD
# Datos de ejemplo (MOCK) - Deberían venir de una base de datos
veterinaria = Veterinaria("VetLog")

mascotas = [
    Paciente(1, "Firulais", "Perro", "Labrador", "Macho", "Marrón", "2020-05-10", True, False, True, 1),
    Paciente(2, "Michi", "Gato", "Siamés", "Hembra", "Blanco", "2021-03-15", True, False, False, 2),
    Paciente(3, "Nemo", "Pez", "Goldfish", "Macho", "Naranja", "2022-01-01", True, False, False, 1)
]

=======
# Definición del Blueprint
>>>>>>> d6b0761 (- Se agrega SQL alchemy con SQL lite)
home_bp = Blueprint("home_bp", __name__)

# Home
@home_bp.route("/", methods=["GET"])
def home():
    veterinaria = Veterinaria("Veterinaria PPS") # TODO: Implementar modelo
    pacientes = Paciente.query.all()
    return render_template("index.html", veterinaria=veterinaria, mascotas=pacientes)

# Detalle de mascota
@home_bp.route("/paciente/<int:id>", methods=["GET"])
<<<<<<< HEAD
def detalle_mascota(id):
<<<<<<< HEAD
<<<<<<< HEAD
    mascota = next((m for m in mascotas if m.id == id), None)
    if mascota:
        return render_template("detalle_mascota.html", mascota=mascota, veterinaria=veterinaria)
    return "Mascota no encontrada", 404
=======
    mascota = Paciente.query.get(id)
    if mascota is not None:
        tutor = Tutor.query.get(mascota.tutor_id)
        return f"Aquí va el detalle de la mascota: {mascota.nombre} y el dueño es {tutor.nombre} {tutor.apellido}"
    return "Mascota no encontrada", 404
>>>>>>> d6b0761 (- Se agrega SQL alchemy con SQL lite)
=======
=======
def detalle_paciente(id):
>>>>>>> 6d90a71 (fix)
    paciente = Paciente.query.get(id)
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return f"Aquí va el detalle de la mascota: {paciente.nombre} y el dueño es {tutor.nombre} {tutor.apellido}"
    return "Mascota no encontrada", 404
>>>>>>> e279ca9 (Fix de nombre de variables)
