# Pet Shop Amigo Fiel

Aplicação web em Flask para cadastrar pets, donos e serviços.
Os serviços podem ser acompanhados pelos status Agendado, Em andamento e Concluído.

## Executar localmente

```bash
git clone URL_DO_REPOSITORIO
cd petshop

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` no navegador.

O banco SQLite `petshop.db` é criado automaticamente na primeira execução.

Para implantação, defina a variável de ambiente `PETSHOP_SECRET_KEY` com uma chave estável. Em execução local, o aplicativo gera uma chave temporária automaticamente.
