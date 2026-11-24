from contextlib import closing
import sqlite3
from pathlib import Path

BANCO = Path(__file__).resolve().parent / "petshop.db"


def contar_registros():
    with closing(sqlite3.connect(BANCO)) as conexao:
        return {
            tabela: conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
            for tabela in ("donos", "pets", "servicos")
        }


def listar_donos():
    consulta = "SELECT nome, tel, email FROM donos ORDER BY nome"
    with closing(sqlite3.connect(BANCO)) as conexao:
        return conexao.execute(consulta).fetchall()


def listar_pets_e_donos():
    consulta = """
        SELECT pets.nome, pets.raca, donos.nome
        FROM pets
        JOIN donos ON pets.dono_id = donos.id
        ORDER BY pets.nome
    """
    with closing(sqlite3.connect(BANCO)) as conexao:
        return conexao.execute(consulta).fetchall()


def listar_servicos():
    consulta = """
        SELECT servicos.tipo, servicos.data, servicos.horario,
               servicos.status, servicos.preco, pets.nome
        FROM servicos
        JOIN pets ON servicos.pet_id = pets.id
        ORDER BY servicos.data, servicos.horario
    """
    with closing(sqlite3.connect(BANCO)) as conexao:
        return conexao.execute(consulta).fetchall()


def buscar_informacoes_contato():
    consulta = """
        SELECT telefone, email, horario, endereco
        FROM informacoes_contato
        WHERE id = 1
    """
    with closing(sqlite3.connect(BANCO)) as conexao:
        return conexao.execute(consulta).fetchone()


if __name__ == "__main__":
    if not BANCO.exists():
        print(f"Banco não encontrado: {BANCO}")
    else:
        print("=== RESUMO DO BANCO ===")
        for tabela, total in contar_registros().items():
            print(f"{tabela.capitalize()}: {total}")

        print("\n=== DONOS ===")
        for nome, telefone, email in listar_donos():
            print(f"  {nome} | Telefone: {telefone} | Email: {email or 'não informado'}")

        print("\n=== PETS E SEUS DONOS ===")
        for pet, raca, dono in listar_pets_e_donos():
            print(f"  {pet} ({raca or 'raça não informada'}) -> {dono}")

        print("\n=== SERVIÇOS ===")
        for tipo, data, horario, status, preco, pet in listar_servicos():
            preco_texto = (
                f"R$ {preco:.2f}".replace(".", ",")
                if preco is not None
                else "preço não informado"
            )
            horario_texto = horario or "horário não informado"
            print(
                f"  {data} {horario_texto} | {tipo} para {pet} | "
                f"{status} | {preco_texto}"
            )

        print("\n=== CONTATO DO PET SHOP ===")
        contato = buscar_informacoes_contato()
        if contato is None:
            print("  Informações de contato não cadastradas.")
        else:
            telefone, email, horario, endereco = contato
            print(f"  Telefone: {telefone}")
            print(f"  Email: {email}")
            print(f"  Horário: {horario}")
            print(f"  Endereço: {endereco}")
