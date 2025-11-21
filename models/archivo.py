from models import db


class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    consulta = db.relationship('Consulta', backref=db.backref('archivos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('archivos', lazy=True))