import sqlite3
from pathlib import Path

BANCO = Path(__file__).resolve().parent / "petshop.db"


def contar_registros():
    with sqlite3.connect(BANCO) as conexao:
        return {
            tabela: conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
            for tabela in ("donos", "pets", "servicos")
        }


def listar_pets_e_donos():
    consulta = """
        SELECT pets.nome, donos.nome
        FROM pets
        JOIN donos ON pets.dono_id = donos.id
    """
    with sqlite3.connect(BANCO) as conexao:
        return conexao.execute(consulta).fetchall()


if __name__ == "__main__":
    if not BANCO.exists():
        print(f"Banco não encontrado: {BANCO}")
    else:
        print("=== RESUMO DO BANCO ===")
        for tabela, total in contar_registros().items():
            print(f"{tabela.capitalize()}: {total}")

        print("\n=== PETS E SEUS DONOS ===")
        for pet, dono in listar_pets_e_donos():
            print(f"  {pet} -> {dono}")
