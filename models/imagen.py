from models import db

class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    paciente = db.relationship('Paciente', backref=db.backref('imagenes', lazy=True))

    def __repr__(self):
        return f'<Imagen {self.id} - {self.url}>'
