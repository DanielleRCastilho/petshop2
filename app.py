import os

from flask import Flask, abort, render_template, request, redirect, url_for
import db_sql
app = Flask(__name__)
db_sql.init_app(app)

db_path = os.path.join(app.root_path, "petshop.db")
if not os.path.exists(db_path):
    with app.app_context():
        db_sql.init_db()

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/sobre")
def sobre():
   return render_template("sobre.html")

@app.route("/servicos")
def servicos():
   return render_template("servicos.html", servicos=db_sql.listar_servicos())

@app.route("/servicos/novo", methods=["GET", "POST"])
def novo_servico():
   pets = db_sql.listar_pets()
   if request.method == "POST":
       if not pets:
           abort(400, description="Cadastre um pet antes de registrar um serviço.")
       db_sql.inserir_servico(
           request.form["tipo"],
           request.form["data"],
           request.form["preco"] or None,
           request.form["pet_id"],
       )
       return redirect(url_for("servicos"))
   return render_template(
       "form_servico.html", servico=None, pets=pets
   )

@app.route("/servico/<int:id>/editar", methods=["GET", "POST"])
def editar_servico(id):
   servico = db_sql.buscar_servico(id)
   if servico is None:
       abort(404)
   pets = db_sql.listar_pets()
   if request.method == "POST":
       db_sql.atualizar_servico(
           id,
           request.form["tipo"],
           request.form["data"],
           request.form["preco"] or None,
           request.form["pet_id"],
       )
       return redirect(url_for("servicos"))
   return render_template("form_servico.html", servico=servico, pets=pets)

@app.route("/servico/<int:id>/excluir", methods=["POST"])
def excluir_servico(id):
   if db_sql.buscar_servico(id) is None:
       abort(404)
   db_sql.excluir_servico(id)
   return redirect(url_for("servicos"))

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
   return render_template("form_dono.html", dono=None)

@app.route("/dono/<int:id>/editar", methods=["GET", "POST"])
def editar_dono(id):
   dono = db_sql.buscar_dono(id)
   if dono is None:
       abort(404)
   if request.method == "POST":
       db_sql.atualizar_dono(
           id,
           request.form["nome"],
           request.form["tel"],
           request.form["email"] or None,
       )
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html", dono=dono)

@app.route("/dono/<int:id>/excluir", methods=["POST"])
def excluir_dono(id):
   if db_sql.buscar_dono(id) is None:
       abort(404)
   db_sql.excluir_dono(id)
   return redirect(url_for("lista_donos"))

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
   pet = db_sql.buscar_pet(id)
   if pet is None:
       abort(404)
   if request.method == "POST":
       db_sql.atualizar_pet(
           id,
           request.form["nome"],
           request.form["raca"],
           request.form["dono_id"],
       )
       return redirect(url_for("pet", id=id))
   return render_template(
       "form_pet.html", pet=pet, donos=db_sql.listar_donos()
   )

@app.route("/pet/<int:id>/excluir", methods=["POST"])
def excluir_pet(id):
   if db_sql.buscar_pet(id) is None:
       abort(404)
   db_sql.excluir_pet(id)
   return redirect(url_for("lista_pets"))

if __name__ == "__main__":
   app.run(debug=True)