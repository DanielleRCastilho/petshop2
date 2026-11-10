from flask import Flask, render_template, request, redirect, url_for
import db_sql
app = Flask(__name__)
db_sql.init_app(app)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/sobre")
def sobre():
   return render_template("sobre.html")

@app.route("/contato")
def contato():
   return render_template("contato.html")

@app.route("/donos")
def lista_donos():
   return render_template("donos.html", donos=db_sql.listar_donos())

@app.route("/donos/novo", methods=["GET", "POST"])
def novo_dono():
   if request.method == "POST":
       db_sql.inserir_dono(
           request.form["nome"],
           request.form["tel"],
           request.form["email"] or None,
       )
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html")

@app.route("/pets")
def lista_pets():
   return render_template("pets.html", pets=db_sql.listar_pets())

@app.route("/pet/<int:id>")
def pet(id):
   return render_template("pet.html", pet=db_sql.buscar_pet(id))

@app.route("/pets/novo", methods=["GET", "POST"])
def novo_pet():
   if request.method == "POST":
       db_sql.inserir_pet(
           request.form["nome"],
           request.form["raca"],
           request.form["dono_id"],
       )
       return redirect(url_for("lista_pets"))
   return render_template("form_pet.html", pet=None, donos=db_sql.listar_donos())

@app.route("/pet/<int:id>/editar", methods=["GET", "POST"])
def editar_pet(id):
   if request.method == "POST":
       db_sql.atualizar_pet(
           id,
           request.form["nome"],
           request.form["raca"],
           request.form["dono_id"],
       )
       return redirect(url_for("pet", id=id))
   return render_template(
       "form_pet.html", pet=db_sql.buscar_pet(id), donos=db_sql.listar_donos()
   )

@app.route("/pet/<int:id>/excluir", methods=["POST"])
def excluir_pet(id):
   db_sql.excluir_pet(id)
   return redirect(url_for("lista_pets"))

if __name__ == "__main__":
   app.run(debug=True)