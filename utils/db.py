from app import app, db
from models.tutor import Tutor
from models.paciente import Paciente
from datetime import date

# Cargar datos de ejemplo en la base de datos
with app.app_context():
    db.drop_all()
    db.create_all()

    t1 = Tutor(nombre="Juan", apellido="Pérez", telefono="123456", email="juan@mail.com", direccion="Calle Falsa 123")
    t2 = Tutor(nombre="Ana", apellido="Gómez", telefono="654321", email="ana@mail.com", direccion="Av. Siempre Viva 742")

    p1 = Paciente(nombre="Firulais", especie="Perro", raza="Labrador", sexo="Macho", color="Marrón",
                  fecha_nacimiento=date(2020, 5, 10), activo=True, reproductor=False, castrado=True, tutor=t1)
    p2 = Paciente(nombre="Michi", especie="Gato", raza="Siamés", sexo="Hembra", color="Blanco",
                  fecha_nacimiento=date(2021, 3, 15), activo=True, reproductor=False, castrado=False, tutor=t2)
    p3 = Paciente(nombre="Nemo", especie="Pez", raza="Goldfish", sexo="Macho", color="Naranja",
                  fecha_nacimiento=date(2025, 1, 1), activo=True, reproductor=False, castrado=False, tutor=t1)

    db.session.add_all([t1, t2, p1, p2])
    db.session.commit()

    print("Datos cargados correctamente")