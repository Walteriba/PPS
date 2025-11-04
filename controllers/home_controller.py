from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import or_ # fix busqueda 
from models.tutor import Tutor
from models.paciente import Paciente
from models.consulta import Consulta
from dto.paciente_dto import PacienteDTO
from models.profesional import Profesional

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


# Ruta raíz - redirige a login si no está autenticado
@home_bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login_page'))
    return redirect(url_for('home_bp.buscar'))


# Busqueda de pacientes y tutores
@home_bp.route("/buscar", methods=["GET"])
@login_required
def buscar():
    # Parámetros de búsqueda
    search_action = request.args.get("search_action") == "1"
    modo = request.args.get("modo", "paciente")
    
    # Filtros de Paciente
    nombre_paciente = request.args.get("nombre_paciente", "").strip()
    especie = request.args.get("especie", "").strip()
    raza = request.args.get("raza", "").strip()
    color = request.args.get("color", "").strip()
    reproductor = request.args.get("reproductor") == "1"
    castrado = request.args.get("castrado") == "1"
    
    # Filtros de Consulta
    anamnesis = request.args.get("anamnesis", "").strip()
    diagnostico = request.args.get("diagnostico", "").strip()
    tratamiento = request.args.get("tratamiento", "").strip()
    
    # Filtros de Tutor
    nombre_tutor = request.args.get("nombre_tutor", "").strip()

    # Lógica de búsqueda
    has_filters = any(
        [
            nombre_paciente,
            especie,
            raza,
            color,
            reproductor,
            castrado,
            anamnesis,
            diagnostico,
            tratamiento,
            nombre_tutor,
        ]
    )

    pacientes = []
    tutores = []

    if has_filters:
        base_query = Paciente.query

        if modo == "paciente":
            pacientes_query = base_query.join(Tutor)
            
            if nombre_paciente:
                pacientes_query = pacientes_query.filter(Paciente.nombre.ilike(f"%{nombre_paciente}%"))                
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
            
            if nombre_paciente:
                pacientes_query = pacientes_query.filter(Paciente.nombre.ilike(f"%{nombre_paciente}%"))                
            if anamnesis:
                pacientes_query = pacientes_query.filter(Consulta.anamnesis.ilike(f"%{anamnesis}%"))
            if diagnostico:
                pacientes_query = pacientes_query.filter(Consulta.diagnostico.ilike(f"%{diagnostico}%"))
            if tratamiento:
                pacientes_query = pacientes_query.filter(Consulta.tratamiento.ilike(f"%{tratamiento}%"))

        elif modo == "tutor":
            pacientes_query = base_query.join(Tutor) 
            
            if nombre_tutor:
                search_words = nombre_tutor.split()
                for word in search_words:
                    pacientes_query = pacientes_query.filter(or_(Tutor.nombre.ilike(f"%{word}%"), Tutor.apellido.ilike(f"%{word}%")))

        pacientes = pacientes_query.options(joinedload(Paciente.tutor)).all()
        tutores = list({p.tutor for p in pacientes if p.tutor})

    # --- DTO ---
    pacientes_dto = CreatePacienteDto(tutores, pacientes)
    
    # --- Parámetros de búsqueda para mantener en el formulario ---
    search = {
        "modo": modo,
        "nombre_paciente": nombre_paciente,
        "especie": especie,
        "raza": raza,
        "color": color,
        "reproductor": bool(reproductor),
        "castrado": bool(castrado),
        "anamnesis": anamnesis,
        "diagnostico": diagnostico,
        "tratamiento": tratamiento,
        "nombre_tutor": nombre_tutor,
        "search_performed": search_action, 
    }
    return render_template("index.html", pacientes=pacientes_dto, search=search)


# Detalle de paciente
@home_bp.route("/paciente/<int:id>", methods=["GET"])
@login_required
def detalle_paciente(id):
    # Obtener paciente y su tutor
    paciente = Paciente.query.get(id)
    if paciente is not None:
        tutor = Tutor.query.get(paciente.tutor_id)
        return render_template("detalle_paciente.html", paciente=paciente, tutor=tutor)
    # Si no se encuentra el paciente, mostrar un mensaje de error
    return "Mascota no encontrada", 404


# GET -> mostrar la vista admin.html con lista de profesionales
@home_bp.route("/admin", methods=["GET"])
@login_required
def admin():
    profesionales = Profesional.query.all() 
    return render_template("admin.html", profesionales=profesionales)