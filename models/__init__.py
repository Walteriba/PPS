from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para que SQLAlchemy los reconozca
from models.tutor import Tutor
from models.paciente import Paciente
from models.consulta import Consulta
from models.archivo import Archivo
from models.profesional import Profesional