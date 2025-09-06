from flask import Flask
from controllers.home_controller import home_bp

app = Flask(__name__)

# Registrar los Blueprint de los controladores
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)