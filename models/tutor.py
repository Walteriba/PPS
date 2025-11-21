from models import db


class Tutor(db.Model):
    __tablename__ = "tutores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    # Relación uno-a-muchos
    pacientes = db.relationship("Paciente", backref="tutor", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('tutores', lazy=True))

    