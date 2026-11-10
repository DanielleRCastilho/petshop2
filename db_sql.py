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
   