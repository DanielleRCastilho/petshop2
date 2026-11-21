import os

from flask import Flask, abort, flash, render_template, request, redirect, url_for
import db_sql
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("PETSHOP_SECRET_KEY") or os.urandom(32)
db_sql.init_app(app)

STATUS_SERVICOS = ("Agendado", "Em andamento", "Concluído")

with app.app_context():
    db_sql.init_db()

@app.route("/")
def index():
   return render_template("index.html", resumo=db_sql.contar_registros())

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
       status = request.form.get("status")
       if status not in STATUS_SERVICOS:
           abort(400, description="Selecione um status válido para o serviço.")
       db_sql.inserir_servico(
           request.form["tipo"],
           request.form["data"],
           request.form["preco"] or None,
           request.form["pet_id"],
           status,
       )
       flash("Serviço cadastrado com sucesso.", "success")
       return redirect(url_for("servicos"))
   return render_template(
       "form_servico.html",
       servico=None,
       pets=pets,
       status_servicos=STATUS_SERVICOS,
   )

@app.route("/servico/<int:id>/editar", methods=["GET", "POST"])
def editar_servico(id):
   servico = db_sql.buscar_servico(id)
   if servico is None:
       abort(404)
   pets = db_sql.listar_pets()
   if request.method == "POST":
       status = request.form.get("status")
       if status not in STATUS_SERVICOS:
           abort(400, description="Selecione um status válido para o serviço.")
       db_sql.atualizar_servico(
           id,
           request.form["tipo"],
           request.form["data"],
           request.form["preco"] or None,
           request.form["pet_id"],
           status,
       )
       flash("Serviço atualizado com sucesso.", "success")
       return redirect(url_for("servicos"))
   return render_template(
       "form_servico.html",
       servico=servico,
       pets=pets,
       status_servicos=STATUS_SERVICOS,
   )

@app.route("/servico/<int:id>/excluir", methods=["POST"])
def excluir_servico(id):
   if db_sql.buscar_servico(id) is None:
       abort(404)
   db_sql.excluir_servico(id)
   flash("Serviço excluído com sucesso.", "success")
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
       flash("Dono cadastrado com sucesso.", "success")
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
       flash("Dono atualizado com sucesso.", "success")
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html", dono=dono)

@app.route("/dono/<int:id>/excluir", methods=["POST"])
def excluir_dono(id):
   if db_sql.buscar_dono(id) is None:
       abort(404)
   db_sql.excluir_dono(id)
   flash("Dono e dados vinculados excluídos com sucesso.", "success")
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
       flash("Pet cadastrado com sucesso.", "success")
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
       flash("Pet atualizado com sucesso.", "success")
       return redirect(url_for("pet", id=id))
   return render_template(
       "form_pet.html", pet=pet, donos=db_sql.listar_donos()
   )

@app.route("/pet/<int:id>/excluir", methods=["POST"])
def excluir_pet(id):
   if db_sql.buscar_pet(id) is None:
       abort(404)
   db_sql.excluir_pet(id)
   flash("Pet e serviços vinculados excluídos com sucesso.", "success")
   return redirect(url_for("lista_pets"))

if __name__ == "__main__":
   app.run(debug=True)