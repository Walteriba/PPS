from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", materia="PPS", lista=["Walter", "Ana", "Damian", "Pablo", "Angel", "Catalina", "Valentin", "Gustavo"])

if __name__ == "__main__":
    app.run(debug=True)