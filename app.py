import os   # Necesario para que funcione {os.environ.get("SECRET_KEY")}
from flask import Flask
from flask_login import LoginManager
from models import db
from models.usuario import Usuario
from controllers.home_controller import home_bp
from controllers.paciente_controller import paciente_bp
from controllers.consulta_controller import consulta_bp
from controllers.tutor_controller import tutor_bp
from controllers.profesional_controller import profesional_bp
from controllers.auth_controller import auth_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetlog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]  # Requiere que la variable de entorno esté configurada
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login_page"  # Ruta a la que redirigir si no hay sesión

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Inicializamos SQLAlchemy con la app
db.init_app(app)

with app.app_context():
    db.create_all()

# Registrar los Blueprint de los controladores
app.register_blueprint(home_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(tutor_bp)
app.register_blueprint(profesional_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
