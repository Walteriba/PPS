import os
from dotenv import load_dotenv
from flask import Flask, request, session
from flask_login import LoginManager
from controllers.auth_controller import auth_bp
from controllers.consulta_controller import consulta_bp
from controllers.paciente_controller import paciente_bp
from controllers.profesional_controller import profesional_bp
from controllers.search_controller import search_bp
from controllers.tutor_controller import tutor_bp
from models import db
from models.usuario import Usuario
from utils.logger import setup_logging

# --- Cargar variables del archivo .env ---
load_dotenv()

# --- Creación de la App ---
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

# --- Configuración del entorno ---
flask_env = os.getenv("FLASK_ENV")
debug_mode = os.getenv("DEBUG").lower() == "true"
secret_key = os.getenv("SECRET_KEY")

app.config["ENV"] = flask_env
app.config["DEBUG"] = debug_mode
app.debug = debug_mode
app.config["SECRET_KEY"] = secret_key

# --- Configuración del Logger ---
setup_logging(app)
app.logger.info(f"Iniciando VetLog en modo {flask_env.upper()} (debug={app.debug})")

# --- Configuración de Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login_page"


# --- Middleware ---
def ensure_theme_in_session():
    if "theme" not in session:
        session["theme"] = "dark"


@app.before_request
def before_request_callbacks():
    ensure_theme_in_session()
    app.logger.debug(
        f"Request: {request.method} {request.path} from {request.remote_addr}"
    )


@app.after_request
def after_request_callbacks(response):
    app.logger.debug(f"Response: {response.status_code}")
    return response


@app.errorhandler(Exception)
def handle_uncaught_exception(e):
    app.logger.error(f"Excepción no controlada: {e}", exc_info=True)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# --- Inicialización de la DB ---
db.init_app(app)
with app.app_context():
    db.create_all()

# --- Registro de Blueprints ---
app.register_blueprint(search_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(tutor_bp)
app.register_blueprint(profesional_bp)
app.register_blueprint(auth_bp)

# --- Ejecución ---
if __name__ == "__main__":
    app.logger.info("Iniciando servidor Flask...")
    app.run(debug=app.debug)
