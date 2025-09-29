import os
from flask import Flask
from . import db, auth, blog

def create_app(test_config=None):
	# Crear y configurar la app
	app = Flask(__name__, instance_relative_config=True) # crea la instancia Flask
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
		)

	if test_config is None:
		# Cargar la configuración de la instancia, si existe,
		# cuando no se esté realizando una prueba.
		app.config.from_pyfile('config.py', silent=True)
	else:
		# cargar la configuración de prueba si se pasa
		app.config.from_mapping(test_config)

	# se asegura de que la carpeta de la instancia exista
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	
	db.init_app(app)
	app.register_blueprint(auth.bp)
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	# pagina simple que saluda
	@app.route('/hello')
	def hello():
		return 'Hola, Mundo!'

	return app