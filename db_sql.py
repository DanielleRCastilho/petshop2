import os
import sqlite3
import click
from flask import current_app, g

def get_db():
   if "db" not in g:
       caminho = os.path.join(current_app.root_path, "petshop.db")
       g.db = sqlite3.connect(caminho)
       g.db.row_factory = sqlite3.Row
       g.db.execute("PRAGMA foreign_keys = ON")
   return g.db

def close_db(e=None):
   db = g.pop("db", None)
   if db is not None:
       db.close()

def init_db():
   db = get_db()
   caminho = os.path.join(current_app.root_path, "schema.sql")
   with open(caminho, encoding="utf-8") as f:
       db.executescript(f.read())

@click.command("init-db")
def init_db_command():
   init_db()
   click.echo("Banco de dados criado com sucesso!")

def init_app(app):
   app.teardown_appcontext(close_db)
   app.cli.add_command(init_db_command)

def inserir_dono(nome, tel, email):
   db = get_db()
   db.execute(
       "INSERT INTO donos (nome, tel, email) VALUES (?, ?, ?)",
       (nome, tel, email),
   )
   db.commit()

def listar_donos():
   return get_db().execute(
       "SELECT id, nome, tel, email FROM donos ORDER BY nome"
   ).fetchall()

def buscar_dono(id):
   return get_db().execute(
       "SELECT id, nome, tel, email FROM donos WHERE id = ?",
       (id,),
   ).fetchone()

def atualizar_dono(id, nome, tel, email):
   db = get_db()
   db.execute(
       "UPDATE donos SET nome = ?, tel = ?, email = ? WHERE id = ?",
       (nome, tel, email, id),
   )
   db.commit()

def excluir_dono(id):
   db = get_db()
   db.execute("DELETE FROM donos WHERE id = ?", (id,))
   db.commit()

def inserir_pet(nome, raca, dono_id):
   db = get_db()
   db.execute(
       "INSERT INTO pets (nome, raca, dono_id) VALUES (?, ?, ?)",
       (nome, raca, dono_id),
   )
   db.commit()

def listar_pets():
   return get_db().execute(
       "SELECT pets.id, pets.nome, pets.raca, donos.nome AS dono "
       "FROM pets INNER JOIN donos ON pets.dono_id = donos.id "
       "ORDER BY pets.nome"
   ).fetchall()

def buscar_pet(id):
   return get_db().execute(
       "SELECT pets.id, pets.nome, pets.raca, pets.dono_id, donos.nome AS dono "
       "FROM pets INNER JOIN donos ON pets.dono_id = donos.id "
       "WHERE pets.id = ?",
       (id,),
   ).fetchone()

def atualizar_pet(id, nome, raca, dono_id):
   db = get_db()
   db.execute(
       "UPDATE pets SET nome = ?, raca = ?, dono_id = ? WHERE id = ?",
       (nome, raca, dono_id, id),
   )
   db.commit()

def excluir_pet(id):
   db = get_db()
   db.execute("DELETE FROM pets WHERE id = ?", (id,))
   db.commit()

def inserir_servico(tipo, data, preco, pet_id):
   db = get_db()
   db.execute(
       "INSERT INTO servicos (tipo, data, preco, pet_id) "
       "VALUES (?, ?, ?, ?)",
       (tipo, data, preco, pet_id),
   )
   db.commit()

def listar_servicos():
   return get_db().execute(
       "SELECT servicos.id, servicos.tipo, servicos.data, servicos.preco, "
       "servicos.pet_id, pets.nome AS pet "
       "FROM servicos INNER JOIN pets ON servicos.pet_id = pets.id "
       "ORDER BY servicos.data DESC, servicos.id DESC"
   ).fetchall()

def buscar_servico(id):
   return get_db().execute(
       "SELECT servicos.id, servicos.tipo, servicos.data, servicos.preco, "
       "servicos.pet_id, pets.nome AS pet "
       "FROM servicos INNER JOIN pets ON servicos.pet_id = pets.id "
       "WHERE servicos.id = ?",
       (id,),
   ).fetchone()

def atualizar_servico(id, tipo, data, preco, pet_id):
   db = get_db()
   db.execute(
       "UPDATE servicos SET tipo = ?, data = ?, preco = ?, pet_id = ? "
       "WHERE id = ?",
       (tipo, data, preco, pet_id, id),
   )
   db.commit()

def excluir_servico(id):
   db = get_db()
   db.execute("DELETE FROM servicos WHERE id = ?", (id,))
   db.commit()
   