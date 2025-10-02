from flask import Flask
from models import db
from controllers.home_controller import home_bp
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from controllers.paciente_controller import paciente_bp
<<<<<<< HEAD
from controllers.consulta_controller import consulta_bp
=======
from utils.cloudinary_utils import subir_y_obtener_url
from flask import request
=======
from utils.cloudinary_utils import subir_y_obtener_url
from flask import request, redirect, url_for, render_template, flash
=======
>>>>>>> 90e2d9e (- Se agrega a model la imagen, en las vistas y en controller)
from controllers.paciente_controller import paciente_bp
>>>>>>> 9ae4b62 (actualizacion_prueba)
=======
from dotenv import load_dotenv
import os 

load_dotenv() 
>>>>>>> 88acec4 (corregi errores de indentacion, importe en el archivo app.py el modulo del archivo .env, para probarlo correctamente hay que cargar las api secret de la cuanta de cloudinary que tengamos)

<<<<<<< HEAD

>>>>>>> 6914ee3 (cloudinary)

=======
>>>>>>> a21801e (- Cambios para probar desde web la subida de archivos)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializamos SQLAlchemy con la app
db.init_app(app)

with app.app_context():
    db.create_all()

# Registrar los Blueprint de los controladores
app.register_blueprint(home_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)

if __name__ == "__main__":
    app.run(debug=True)