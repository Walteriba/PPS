from models import db


class Profesional(db.Model):
    """Definición de la clase Profesional."""
    __tablename__ = "profesionales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    matricula = db.Column(db.String(50), nullable=True)
    especialidad = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('profesionales', lazy=True))

