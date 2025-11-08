from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.archivo import Archivo
from models.consulta import Consulta
from models.paciente import Paciente
from models.profesional import Profesional
from models.tutor import Tutor
