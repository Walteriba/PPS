"""Modelo de datos para la entidad Profesional."""
from models import db

class Profesional(db.Model):
    """Definición de la clase Profesional."""
    __tablename__ = "profesionales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    matricula = db.Column(db.String(50), nullable=False, unique=True)
    especialidad = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
