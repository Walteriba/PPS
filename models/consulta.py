from models import db
from datetime import date


class Consulta(db.Model):
    __tablename__ = "consultas"

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutores.id"), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    fecha = db.Column(db.Date, default=date.today)
    peso = db.Column(db.Float, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    anamnesis = db.Column(db.String(400), nullable=True)
    examen_fisico = db.Column(db.String(512), nullable=True)
    diagnostico = db.Column(db.String(200), nullable=True)
    tratamiento = db.Column(db.String(400), nullable=True)

    # Relaciones uno a muchos
    paciente_id = db.relationship("Paciente", backref="consultas", lazy=True)
    tutor_id = db.relationship("Tutor", backref="consultas", lazy=True)
        