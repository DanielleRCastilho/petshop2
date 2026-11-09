from flask import Flask, render_template

import db_sql

app = Flask(__name__)

db_sql.init_app(app)

pets = [
    {"id": 1, "nome": "Rex", "especie": "Cachorro", "dono": "Ana"},
    {"id": 2, "nome": "Mia", "especie": "Gato", "dono": "Carlos"},
    {"id": 3, "nome": "Thor", "especie": "Cachorro", "dono": "Julia"},
    {"id": 4, "nome": "Luna", "especie": "Gato", "dono": "Pedro"},
    {"id": 5, "nome": "Bob", "especie": "Cachorro", "dono": "Mariana"},
    {"id": 6, "nome": "Nina", "especie": "Coelho", "dono": "Lucas"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/pets")
def lista_pets():
    return render_template("pets.html", pets=pets)

@app.route("/pet/<int:id>")
def pet(id):
    pet = next((p for p in pets if p["id"] == id), None)
    return render_template("pet.html", pet=pet)

if __name__ == "__main__":
    app.run(debug=True)
