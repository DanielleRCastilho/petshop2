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