from models import db

class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=True)
    
    consulta = db.relationship('Consulta', backref=db.backref('archivos', lazy=True))

    def __repr__(self):
        return f'<Archivo {self.id} - {self.url}>'
