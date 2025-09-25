from flask import Flask
from models import db
from controllers.home_controller import home_bp
from utils.cloudinary_utils import subir_y_obtener_url
from flask import request, redirect, url_for, render_template, flash
from controllers.paciente_controller import paciente_bp

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

if __name__ == "__main__":
    app.run(debug=True)