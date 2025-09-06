from flask import Flask, render_template, request

app = Flask(__name__)

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