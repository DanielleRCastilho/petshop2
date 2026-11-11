from datetime import date
import math
import sqlite3
from flask import Flask, abort, render_template, request, redirect, url_for
import db_sql
app = Flask(__name__)
db_sql.init_app(app)

with app.app_context():
   db_sql.init_db()

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
       nome = request.form["nome"].strip()
       tel = request.form.get("tel", "").strip() or None
       email = request.form.get("email", "").strip() or None
       try:
           db_sql.inserir_dono(nome, tel, email)
       except sqlite3.IntegrityError:
           return render_template(
               "form_dono.html",
               erro="Este e-mail já está cadastrado.",
               nome=nome,
               tel=tel or "",
               email=email or "",
           ), 400
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html")

@app.route("/donos/<int:id>/editar", methods=["GET", "POST"])
def editar_dono(id):
   dono = db_sql.buscar_dono(id)
   if dono is None:
       abort(404)
   if request.method == "POST":
       nome = request.form["nome"].strip()
       tel = request.form.get("tel", "").strip() or None
       email = request.form.get("email", "").strip() or None
       try:
           db_sql.atualizar_dono(id, nome, tel, email)
       except sqlite3.IntegrityError:
           return render_template(
               "form_dono.html",
               dono=dono,
               erro="Este e-mail já está cadastrado.",
               nome=nome,
               tel=tel or "",
               email=email or "",
           ), 400
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html", dono=dono)

@app.route("/donos/<int:id>/excluir", methods=["POST"])
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
   donos = db_sql.listar_donos()
   if request.method == "POST":
       dono_id = request.form.get("dono_id", type=int)
       if dono_id is None or db_sql.buscar_dono(dono_id) is None:
           return render_template(
               "form_pet.html",
               pet=None,
               donos=donos,
               erro="Selecione um dono cadastrado.",
           ), 400
       db_sql.inserir_pet(
           request.form["nome"],
           request.form["raca"],
           dono_id,
       )
       return redirect(url_for("lista_pets"))
   return render_template("form_pet.html", pet=None, donos=donos)

@app.route("/pet/<int:id>/editar", methods=["GET", "POST"])
def editar_pet(id):
   registro = db_sql.buscar_pet(id)
   if registro is None:
       abort(404)
   donos = db_sql.listar_donos()
   if request.method == "POST":
       dono_id = request.form.get("dono_id", type=int)
       if dono_id is None or db_sql.buscar_dono(dono_id) is None:
           return render_template(
               "form_pet.html",
               pet=registro,
               donos=donos,
               erro="Selecione um dono cadastrado.",
           ), 400
       db_sql.atualizar_pet(
           id,
           request.form["nome"],
           request.form["raca"],
           dono_id,
       )
       return redirect(url_for("pet", id=id))
   return render_template("form_pet.html", pet=registro, donos=donos)

@app.route("/pet/<int:id>/excluir", methods=["POST"])
def excluir_pet(id):
   if db_sql.buscar_pet(id) is None:
       abort(404)
   db_sql.excluir_pet(id)
   return redirect(url_for("lista_pets"))

def _dados_servico_formulario():
   tipo = request.form.get("tipo", "").strip()
   data = request.form.get("data", "")
   date.fromisoformat(data)
   preco_texto = request.form.get("preco", "").strip()
   preco = float(preco_texto) if preco_texto else None
   pet_id = request.form.get("pet_id", type=int)
   if (
       not tipo
       or (preco is not None and (not math.isfinite(preco) or preco < 0))
       or pet_id is None
       or db_sql.buscar_pet(pet_id) is None
   ):
       raise ValueError("Dados do serviço inválidos.")
   return tipo, data, preco, pet_id

@app.route("/servicos")
def lista_servicos():
   return render_template("servicos.html", servicos=db_sql.listar_servicos())

@app.route("/servicos/novo", methods=["GET", "POST"])
def novo_servico():
   if request.method == "POST":
       try:
           tipo, data, preco, pet_id = _dados_servico_formulario()
       except ValueError:
           return render_template(
               "form_servico.html",
               servico=None,
               pets=db_sql.listar_pets(),
               erro="Preencha os campos corretamente e selecione um pet cadastrado.",
           ), 400
       db_sql.inserir_servico(tipo, data, preco, pet_id)
       return redirect(url_for("lista_servicos"))
   return render_template(
       "form_servico.html", servico=None, pets=db_sql.listar_pets()
   )

@app.route("/servico/<int:id>")
def servico(id):
   registro = db_sql.buscar_servico(id)
   if registro is None:
       abort(404)
   return render_template("servico.html", servico=registro)

@app.route("/servico/<int:id>/editar", methods=["GET", "POST"])
def editar_servico(id):
   registro = db_sql.buscar_servico(id)
   if registro is None:
       abort(404)
   if request.method == "POST":
       try:
           tipo, data, preco, pet_id = _dados_servico_formulario()
       except ValueError:
           return render_template(
               "form_servico.html",
               servico=registro,
               pets=db_sql.listar_pets(),
               erro="Preencha os campos corretamente e selecione um pet cadastrado.",
           ), 400
       db_sql.atualizar_servico(id, tipo, data, preco, pet_id)
       return redirect(url_for("servico", id=id))
   return render_template(
       "form_servico.html", servico=registro, pets=db_sql.listar_pets()
   )

@app.route("/servico/<int:id>/excluir", methods=["POST"])
def excluir_servico(id):
   if db_sql.buscar_servico(id) is None:
       abort(404)
   db_sql.excluir_servico(id)
   return redirect(url_for("lista_servicos"))

if __name__ == "__main__":
   app.run(debug=True)