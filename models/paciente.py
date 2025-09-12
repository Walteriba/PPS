from models import db
from datetime import date

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, default=date.today)
    ##foto = db.Column(db.String(), nullable=True) #TODO: Implementar
    activo = db.Column(db.Boolean, default=True)
    reproductor = db.Column(db.Boolean, default=False)
    castrado = db.Column(db.Boolean, default=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutores.id"), nullable=False)