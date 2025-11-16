import os
from flask import Flask, session
from dotenv import load_dotenv
from flask_login import LoginManager
from controllers.auth_controller import auth_bp
from controllers.consulta_controller import consulta_bp
from controllers.paciente_controller import paciente_bp
from controllers.profesional_controller import profesional_bp
from controllers.search_controller import search_bp
from controllers.tutor_controller import tutor_bp
from models import db
from models.usuario import Usuario
 
load_dotenv()
 
app = Flask(__name__)
 
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL. Asegúrate de definirla en el archivo .env")
 
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No se encontró la variable de entorno SECRET_KEY. Asegúrate de definirla en el archivo .env")
 
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = (
    "auth_bp.login_page"  # Ruta a la que redirigir si no hay sesión
)

def ensure_theme_in_session():
    if "theme" not in session:
        session["theme"] = "dark"
        
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Inicializamos SQLAlchemy con la app
db.init_app(app)

# Registrar los Blueprint de los controladores
app.register_blueprint(search_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(tutor_bp)
app.register_blueprint(profesional_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
