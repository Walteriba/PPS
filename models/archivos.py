from . import db



class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=True)
    
    paciente = db.relationship('Paciente', backref=db.backref('archivos', lazy=True))
    consulta = db.relationship('Consulta', backref=db.backref('archivos', lazy=True))

    def __repr__(self):
        return f'<Archivo {self.id} - {self.url}>'
