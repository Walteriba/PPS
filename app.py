from flask import Flask
from models import db
from controllers.home_controller import home_bp
<<<<<<< HEAD
from controllers.paciente_controller import paciente_bp
from controllers.consulta_controller import consulta_bp
=======
from utils.cloudinary_utils import subir_y_obtener_url
from flask import request, redirect, url_for, render_template, flash


>>>>>>> 6914ee3 (cloudinary)

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
    
    
    
    
#damian
@app.route('/subir_estudio', methods=['GET', 'POST'])
def subir_estudio():
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if archivo:
            ruta_local = f"static/temp/{archivo.filename}"
            archivo.save(ruta_local)
            url = subir_y_obtener_url(ruta_local, f"estudio_{archivo.filename}")
            # Aquí puedes guardar la URL en la base de datos, asociada al paciente
            flash(f"Imagen subida correctamente: {url}")
            return redirect(url_for('subir_estudio'))
        else:
            flash("No se recibió ningún archivo")
    return render_template('subir_estudio.html')
