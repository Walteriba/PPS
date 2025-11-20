"""Script para cargar datos de ejemplo en la base de datos."""

from datetime import date, timedelta
from random import choice, randint, uniform

from app import app, db
from models.consulta import Consulta
from models.paciente import Paciente
from models.profesional import Profesional
from models.tutor import Tutor
from models.usuario import Usuario


# Datos de ejemplo
nombres_tutores = [
    ("Carlos", "Rodríguez"),
    ("María", "López"),
    ("Jorge", "González"),
    ("Laura", "Martínez"),
    ("Roberto", "Sánchez"),
    ("Ana", "Fernández"),
    ("Diego", "Torres"),
    ("Paula", "Díaz"),
    ("Miguel", "Ruiz"),
    ("Lucía", "García"),
    ("Martín", "Weber"),
    ("Valentina", "Castro"),
    ("Federico", "Morales"),
    ("Camila", "Ortiz"),
    ("Eduardo", "Silva"),
]

nombres_mascotas = [
    "Luna",
    "Max",
    "Nina",
    "Zeus",
    "Lola",
    "Toby",
    "Milo",
    "Coco",
    "Bella",
    "Rocky",
    "Simba",
    "Nala",
    "Thor",
    "Kira",
    "Oliver",
]

especies = {
    "Canino": ["Labrador", "Bulldog", "Pastor Alemán", "Golden", "Mestizo"],
    "Felino": ["Siamés", "Persa", "Angora", "Mestizo", "Maine Coon"],
    "Roedor": ["Holandés", "Rex", "Angora", "Californiano"],
    "Ave": ["Canario", "Periquito", "Agapornis", "Cacatúa"],
}

colores = ["Negro", "Blanco", "Marrón", "Gris", "Manchado", "Atigrado"]

# Datos de ejemplo para profesionales
nombres_profesionales = [
    ("Martina", "Pérez"),
    ("Lorena", "Gómez"),
    ("Julián", "Alvarez"),
    ("Sofía", "Gala"),
    ("Diego", "Suarez"),
]

especialidades = ["Cardiología", "Veterinario"]

# Cargar datos de ejemplo en la base de datos
with app.app_context():
    db.drop_all()
    db.create_all()

    # Crear un usuario por defecto
    usuario = Usuario(
        nombre="Usuario de Prueba",
        email="test@example.com",
    )
    usuario.set_password("password")
    db.session.add(usuario)
    db.session.commit()

    # Crear y guardar profesionales
    profesionales = []
    
    for i, (nombre, apellido) in enumerate(nombres_profesionales):
        profesional = Profesional(
          nombre=nombre,
          apellido=apellido,
          matricula=f"M-{randint(1000,9999)}",
          especialidad=choice(especialidades),
          telefono=f"11{randint(40000000,49999999)}",
          email=f"{nombre.lower()}.{apellido.lower()}@mail.com",
          user_id=usuario.id,
        )
        profesionales.append(profesional)

    db.session.add_all(profesionales)
    db.session.commit()

    # Crear y guardar tutores primero
    tutores = []
    for nombre, apellido in nombres_tutores:
        tutor = Tutor(
            nombre=nombre,
            apellido=apellido,
            telefono=f"15{randint(40000000, 49999999)}",
            email=f"{nombre.lower()}.{apellido.lower()}@mail.com",
            direccion=f"Calle {randint(100, 999)} N°{randint(1000, 9999)}",
            user_id=usuario.id,
        )
        tutores.append(tutor)
    db.session.add_all(tutores)
    db.session.commit()  # Commit tutores primero

    # Crear y guardar pacientes
    pacientes = []
    for nombre in nombres_mascotas:
        especie = choice(list(especies.keys()))
        paciente = Paciente(
            nombre=nombre,
            especie=especie,
            raza=choice(especies[especie]),
            sexo=choice(["Macho", "Hembra"]),
            color=choice(colores),
            fecha_nacimiento=date.today() - timedelta(days=randint(180, 3650)),
            imagen="/static/imgs/default-avatar.jpg",
            activo=True,
            reproductor=choice([True, False]),
            castrado=choice([True, False]),
            tutor_id=choice(tutores).id,  # Usar el ID del tutor ya guardado
            user_id=usuario.id,
        )
        pacientes.append(paciente)
    db.session.add_all(pacientes)
    db.session.commit()  # Commit pacientes antes de crear consultas

    # Crear consultas usando los IDs ya guardados
    consultas = []
    motivos = [
        "Control anual",
        "Vacunación",
        "Malestar general",
        "Problemas digestivos",
        "Control post operatorio",
    ]

    for _ in range(15):
        paciente = choice(pacientes)
        consulta = Consulta(
            fecha=date.today() - timedelta(days=randint(1, 365)),
            peso=round(uniform(2.5, 35.0), 1),
            temperatura=round(uniform(37.5, 40.2), 1),
            anamnesis=f"MOTIVO DE CONSULTA: {choice(motivos)}. PACIENTE PRESENTA {choice(['vómitos', 'diarrea', 'decaimiento', 'tos', 'fiebre'])} DESDE HACE {randint(1,5)} DÍAS.",
            examen_fisico=f"MUCOSAS {choice(['ROSADAS', 'PÁLIDAS'])}, {choice(['CON', 'SIN'])} DESHIDRATACIÓN. FC: {randint(60,120)} lpm, FR: {randint(15,30)} rpm. AUSCULTACIÓN {choice(['NORMAL', 'CON PARTICULARIDADES'])}.",
            diagnostico=f"DIAGNÓSTICO PRESUNTIVO: {choice(['GASTROENTERITIS', 'TRAQUEOBRONQUITIS', 'DERMATITIS', 'OTITIS'])} - PRONÓSTICO {choice(['FAVORABLE', 'RESERVADO'])}",
            tratamiento=f"SE INDICA: {choice(['ANTIBIÓTICOS', 'ANTIINFLAMATORIOS', 'PROTECTOR GÁSTRICO'])} CADA {randint(8,24)}HS POR {randint(5,10)} DÍAS.",
            tutor_id=paciente.tutor_id,  # Usar el ID del tutor del paciente
            paciente_id=paciente.id,
            profesional_id=choice(profesionales).id,
            user_id=usuario.id,
        )
        consultas.append(consulta)

    db.session.add_all(consultas)
    db.session.commit()  # Commit final de consultas
    
    print("Se cargaron exitosamente:")
    print(f"- {len(tutores)} tutores")
    print(f"- {len(pacientes)} pacientes")
    print(f"- {len(consultas)} consultas")
    print(f"- {len(profesionales)} profesionales")


