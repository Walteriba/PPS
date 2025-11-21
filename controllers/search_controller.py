from flask import Blueprint, render_template, request#, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from dto.paciente_dto import PacienteDTO
from models.consulta import Consulta
from models.paciente import Paciente
from models.tutor import Tutor

search_bp = Blueprint("search_bp", __name__)


# Métodos Auxiliares
def CreatePacienteDto(pacientes):
    pacientes_dto = []
    for paciente in pacientes:
        pacientes_dto.append(
            PacienteDTO(
                id=paciente.id,
                imagen=paciente.imagen,
                nombre=paciente.nombre,
                especie=paciente.especie,
                raza=paciente.raza,
                tutor=f"{paciente.tutor.nombre} {paciente.tutor.apellido}",
            )
        )
    return pacientes_dto


@search_bp.route("/buscar", methods=["GET"])
@login_required
def buscar():
    search_action = request.args.get("search_action") == "1"
    modo = request.args.get("modo", "paciente")

    # Filtros de Paciente
    nombre_paciente = request.args.get("nombre_paciente", "").strip()
    especie = request.args.get("especie", "").strip()
    traer_todos_especies = especie == "all"
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
    pacientes = []

    has_filters = any(
        [
            nombre_paciente,
            especie not in ["", "all"],
            raza,
            color,
            reproductor,
            castrado,
            anamnesis,
            diagnostico,
            tratamiento,
            nombre_tutor,
            traer_todos_especies,
        ]
    )

    if has_filters:
        base_query = Paciente.query.filter(Paciente.user_id == current_user.id)

        if modo == "paciente":
            pacientes_query = base_query.join(Tutor)

            if nombre_paciente:
                pacientes_query = pacientes_query.filter(
                    Paciente.nombre.ilike(f"%{nombre_paciente}%")
                )
            if especie and especie != "all":
                pacientes_query = pacientes_query.filter(
                    Paciente.especie.ilike(f"%{especie}%")
                )
            if raza:
                pacientes_query = pacientes_query.filter(
                    Paciente.raza.ilike(f"%{raza}%")
                )
            if color:
                pacientes_query = pacientes_query.filter(
                    Paciente.color.ilike(f"%{color}%")
                )
            if reproductor:
                pacientes_query = pacientes_query.filter(Paciente.reproductor.is_(True))
            if castrado:
                pacientes_query = pacientes_query.filter(Paciente.castrado.is_(True))

        elif modo == "consulta":
            pacientes_query = base_query.join(Consulta).join(Tutor)

            if nombre_paciente:
                pacientes_query = pacientes_query.filter(
                    Paciente.nombre.ilike(f"%{nombre_paciente}%")
                )
            if anamnesis:
                pacientes_query = pacientes_query.filter(
                    Consulta.anamnesis.ilike(f"%{anamnesis}%")
                )
            if diagnostico:
                pacientes_query = pacientes_query.filter(
                    Consulta.diagnostico.ilike(f"%{diagnostico}%")
                )
            if tratamiento:
                pacientes_query = pacientes_query.filter(
                    Consulta.tratamiento.ilike(f"%{tratamiento}%")
                )

        elif modo == "tutor":
            pacientes_query = base_query.join(Tutor)

            if nombre_tutor:
                search_words = nombre_tutor.split()
                for word in search_words:
                    pacientes_query = pacientes_query.filter(
                        or_(
                            Tutor.nombre.ilike(f"%{word}%"),
                            Tutor.apellido.ilike(f"%{word}%"),
                        )
                    )

        pacientes = pacientes_query.options(joinedload(Paciente.tutor)).all()

    # --- DTO ---
    pacientes_dto = CreatePacienteDto(pacientes)

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
