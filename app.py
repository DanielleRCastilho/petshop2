import os
import sqlite3
from datetime import date, time

from flask import Flask, abort, flash, render_template, request, redirect, url_for
import db_sql

TIPOS_SERVICOS = ("Banho", "Tosa", "Consultas", "Cuidados gerais")
STATUS_SERVICOS = ("Agendado", "Em andamento", "Concluído")


def create_app(test_config=None):
   app = Flask(__name__)
   app.config["SECRET_KEY"] = os.environ.get("PETSHOP_SECRET_KEY") or os.urandom(32)
   app.config["SQL_DATABASE"] = os.path.join(app.root_path, "petshop.db")

   if test_config:
       app.config.update(test_config)

   db_sql.init_app(app)
   _register_routes(app)
   with app.app_context():
       db_sql.init_db()
   return app


def campo_obrigatorio(nome, campo=""):
   valor = (campo or "").strip()
   if not valor:
       abort(400, description=f"O campo {nome} é obrigatório.")
   return valor


def validar_data(valor):
   valor = campo_obrigatorio("Data", valor)
   try:
       date.fromisoformat(valor)
   except ValueError:
       abort(400, description="Informe uma data válida.")
   return valor


def validar_horario(valor):
   valor = campo_obrigatorio("Horário", valor)
   try:
       horario = time.fromisoformat(valor)
   except ValueError:
       abort(400, description="Informe um horário válido.")
   if horario.strftime("%H:%M") != valor:
       abort(400, description="Informe um horário válido.")
   return valor


def validar_preco(valor):
   if not (valor or "").strip():
       return None
   try:
       preco = float(valor)
   except ValueError:
       abort(400, description="Informe um preço válido.")
   if preco < 0:
       abort(400, description="O preço não pode ser negativo.")
   return preco


def validar_id(valor, nome, busca):
   try:
       id = int(valor)
   except (TypeError, ValueError):
       abort(400, description=f"Selecione um {nome} válido.")
   if busca(id) is None:
       abort(400, description=f"Selecione um {nome} válido.")
   return id


def index():
   return render_template("index.html", resumo=db_sql.contar_registros())

def sobre():
   return render_template("sobre.html")

def servicos():
   return render_template("servicos.html", servicos=db_sql.listar_servicos())

def novo_servico():
   pets = db_sql.listar_pets()
   if request.method == "POST":
       if not pets:
           abort(400, description="Cadastre um pet antes de registrar um serviço.")
       tipo = campo_obrigatorio("Tipo de serviço", request.form.get("tipo"))
       if tipo not in TIPOS_SERVICOS:
           abort(400, description="Selecione um tipo de serviço válido.")
       status = request.form.get("status")
       if status not in STATUS_SERVICOS:
           abort(400, description="Selecione um status válido para o serviço.")
       data = validar_data(request.form.get("data"))
       horario = validar_horario(request.form.get("horario"))
       preco = validar_preco(request.form.get("preco"))
       pet_id = validar_id(request.form.get("pet_id"), "pet", db_sql.buscar_pet)
       db_sql.inserir_servico(
           tipo,
           data,
           horario,
           preco,
           pet_id,
           status,
       )
       flash("Serviço cadastrado com sucesso.", "success")
       return redirect(url_for("servicos"))
   return render_template(
       "form_servico.html",
       servico=None,
       pets=pets,
       tipos_servicos=TIPOS_SERVICOS,
       status_servicos=STATUS_SERVICOS,
   )

def editar_servico(id):
   servico = db_sql.buscar_servico(id)
   if servico is None:
       abort(404)
   pets = db_sql.listar_pets()
   if request.method == "POST":
       tipo = campo_obrigatorio("Tipo de serviço", request.form.get("tipo"))
       if tipo not in TIPOS_SERVICOS:
           abort(400, description="Selecione um tipo de serviço válido.")
       status = request.form.get("status")
       if status not in STATUS_SERVICOS:
           abort(400, description="Selecione um status válido para o serviço.")
       data = validar_data(request.form.get("data"))
       horario = validar_horario(request.form.get("horario"))
       preco = validar_preco(request.form.get("preco"))
       pet_id = validar_id(request.form.get("pet_id"), "pet", db_sql.buscar_pet)
       db_sql.atualizar_servico(
           id,
           tipo,
           data,
           horario,
           preco,
           pet_id,
           status,
       )
       flash("Serviço atualizado com sucesso.", "success")
       return redirect(url_for("servicos"))
   return render_template(
       "form_servico.html",
       servico=servico,
       pets=pets,
       tipos_servicos=TIPOS_SERVICOS,
       status_servicos=STATUS_SERVICOS,
   )

def excluir_servico(id):
   if db_sql.buscar_servico(id) is None:
       abort(404)
   db_sql.excluir_servico(id)
   flash("Serviço excluído com sucesso.", "success")
   return redirect(url_for("servicos"))

def contato():
   return render_template("contato.html", info=db_sql.buscar_informacoes_contato())

def editar_contato():
   if request.method == "POST":
       telefone = campo_obrigatorio("Telefone", request.form.get("telefone"))
       email = campo_obrigatorio("Email", request.form.get("email"))
       horario = campo_obrigatorio("Horário", request.form.get("horario"))
       endereco = campo_obrigatorio("Endereço", request.form.get("endereco"))
       if len(email) > 254:
           abort(400, description="O email deve ter no máximo 254 caracteres.")
       db_sql.atualizar_informacoes_contato(
           telefone,
           email,
           horario,
           endereco,
       )
       flash("Informações de contato atualizadas com sucesso.", "success")
       return redirect(url_for("contato"))
   return render_template(
       "form_contato.html",
       info=db_sql.buscar_informacoes_contato(),
   )

def lista_donos():
   return render_template("donos.html", donos=db_sql.listar_donos())

def novo_dono():
   if request.method == "POST":
       nome = campo_obrigatorio("Nome", request.form.get("nome"))
       tel = campo_obrigatorio("Telefone", request.form.get("tel"))
       email = (request.form.get("email") or "").strip() or None
       if len(tel) > 15:
           abort(400, description="O telefone deve ter no máximo 15 caracteres.")
       if email and len(email) > 254:
           abort(400, description="O email deve ter no máximo 254 caracteres.")
       if db_sql.buscar_dono_por_telefone(tel):
           flash("Este telefone já está cadastrado.", "error")
           return redirect(url_for("novo_dono"))
       if email and db_sql.buscar_dono_por_email(email):
           flash("Este email já está cadastrado.", "error")
           return redirect(url_for("novo_dono"))
       try:
           db_sql.inserir_dono(nome, tel, email)
       except sqlite3.IntegrityError:
           flash("Este email já está cadastrado.", "error")
           return redirect(url_for("novo_dono"))
       flash("Dono cadastrado com sucesso.", "success")
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html", dono=None)

def editar_dono(id):
   dono = db_sql.buscar_dono(id)
   if dono is None:
       abort(404)
   if request.method == "POST":
       nome = campo_obrigatorio("Nome", request.form.get("nome"))
       tel = campo_obrigatorio("Telefone", request.form.get("tel"))
       email = (request.form.get("email") or "").strip() or None
       if len(tel) > 15:
           abort(400, description="O telefone deve ter no máximo 15 caracteres.")
       if email and len(email) > 254:
           abort(400, description="O email deve ter no máximo 254 caracteres.")
       if db_sql.buscar_dono_por_telefone(tel, exceto_id=id):
           flash("Este telefone já está cadastrado.", "error")
           return redirect(url_for("editar_dono", id=id))
       if email and db_sql.buscar_dono_por_email(email, exceto_id=id):
           flash("Este email já está cadastrado.", "error")
           return redirect(url_for("editar_dono", id=id))
       try:
           db_sql.atualizar_dono(id, nome, tel, email)
       except sqlite3.IntegrityError:
           flash("Este email já está cadastrado.", "error")
           return redirect(url_for("editar_dono", id=id))
       flash("Dono atualizado com sucesso.", "success")
       return redirect(url_for("lista_donos"))
   return render_template("form_dono.html", dono=dono)

def excluir_dono(id):
   if db_sql.buscar_dono(id) is None:
       abort(404)
   db_sql.excluir_dono(id)
   flash("Dono e dados vinculados excluídos com sucesso.", "success")
   return redirect(url_for("lista_donos"))

def lista_pets():
   return render_template("pets.html", pets=db_sql.listar_pets())

def pet(id):
   pet = db_sql.buscar_pet(id)
   if pet is None:
       abort(404)
   return render_template("pet.html", pet=pet)

def novo_pet():
   if request.method == "POST":
       nome = campo_obrigatorio("Nome do pet", request.form.get("nome"))
       raca = (request.form.get("raca") or "").strip() or None
       dono_id = validar_id(request.form.get("dono_id"), "dono", db_sql.buscar_dono)
       db_sql.inserir_pet(
           nome,
           raca,
           dono_id,
       )
       flash("Pet cadastrado com sucesso.", "success")
       return redirect(url_for("lista_pets"))
   return render_template("form_pet.html", pet=None, donos=db_sql.listar_donos())

def editar_pet(id):
   pet = db_sql.buscar_pet(id)
   if pet is None:
       abort(404)
   if request.method == "POST":
       nome = campo_obrigatorio("Nome do pet", request.form.get("nome"))
       raca = (request.form.get("raca") or "").strip() or None
       dono_id = validar_id(request.form.get("dono_id"), "dono", db_sql.buscar_dono)
       db_sql.atualizar_pet(
           id,
           nome,
           raca,
           dono_id,
       )
       flash("Pet atualizado com sucesso.", "success")
       return redirect(url_for("pet", id=id))
   return render_template(
       "form_pet.html", pet=pet, donos=db_sql.listar_donos()
   )

def excluir_pet(id):
   if db_sql.buscar_pet(id) is None:
       abort(404)
   db_sql.excluir_pet(id)
   flash("Pet e serviços vinculados excluídos com sucesso.", "success")
   return redirect(url_for("lista_pets"))


def _register_routes(app):
   app.add_url_rule("/", view_func=index)
   app.add_url_rule("/sobre", view_func=sobre)
   app.add_url_rule("/servicos", view_func=servicos)
   app.add_url_rule("/servicos/novo", view_func=novo_servico, methods=["GET", "POST"])
   app.add_url_rule("/servico/<int:id>/editar", view_func=editar_servico, methods=["GET", "POST"])
   app.add_url_rule("/servico/<int:id>/excluir", view_func=excluir_servico, methods=["POST"])
   app.add_url_rule("/contato", view_func=contato)
   app.add_url_rule(
       "/contato/editar",
       view_func=editar_contato,
       methods=["GET", "POST"],
   )
   app.add_url_rule("/donos", view_func=lista_donos)
   app.add_url_rule("/donos/novo", view_func=novo_dono, methods=["GET", "POST"])
   app.add_url_rule("/dono/<int:id>/editar", view_func=editar_dono, methods=["GET", "POST"])
   app.add_url_rule("/dono/<int:id>/excluir", view_func=excluir_dono, methods=["POST"])
   app.add_url_rule("/pets", view_func=lista_pets)
   app.add_url_rule("/pet/<int:id>", view_func=pet)
   app.add_url_rule("/pets/novo", view_func=novo_pet, methods=["GET", "POST"])
   app.add_url_rule("/pet/<int:id>/editar", view_func=editar_pet, methods=["GET", "POST"])
   app.add_url_rule("/pet/<int:id>/excluir", view_func=excluir_pet, methods=["POST"])


app = create_app()


if __name__ == "__main__":
   app.run(debug=True)