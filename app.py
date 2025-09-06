from flask import Flask, render_template, request

app = Flask(__name__)

# Clases

class Dueno:
    def __init__(self, id, nombre, telefono):
        self.id = id
        self.nombre = nombre
        self.mascotas = []  # lista de ids de mascotas?

class Mascota:
    def __init__(self, id, nombre, especie, edad, dueno_id):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.dueno_id = dueno_id

# Rutas
@app.route("/")
def home():
    return render_template("index.html", materia="PPS", lista=["Walter", "Ana", "Damian", "Pablo", "Angel", "Catalina", "Valentin", "Gustavo"])

@app.route("/formulario", methods=["GET"])
def home_get():
    return render_template("formulario.html")

@app.route("/formulario", methods=["POST"])
def home_post():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    return render_template("resultado.html", nombre=nombre, email=email)

if __name__ == "__main__":
    app.run(debug=True)