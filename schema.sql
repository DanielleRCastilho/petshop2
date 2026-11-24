CREATE TABLE IF NOT EXISTS donos (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome TEXT NOT NULL,
   tel TEXT NOT NULL UNIQUE,
   email TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS pets (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome TEXT NOT NULL,
   raca TEXT,
   dono_id INTEGER NOT NULL,
   FOREIGN KEY (dono_id) REFERENCES donos(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS servicos (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   tipo TEXT NOT NULL
       CHECK (tipo IN ('Banho', 'Tosa', 'Consultas', 'Cuidados gerais')),
   data TEXT NOT NULL,
   horario TEXT,
   preco REAL CHECK (preco IS NULL OR preco >= 0),
   status TEXT NOT NULL DEFAULT 'Agendado'
       CHECK (status IN ('Agendado', 'Em andamento', 'Concluído')),
   pet_id INTEGER NOT NULL,
   FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS informacoes_contato (
   id INTEGER PRIMARY KEY CHECK (id = 1),
   telefone TEXT NOT NULL,
   email TEXT NOT NULL,
   horario TEXT NOT NULL,
   endereco TEXT NOT NULL
);
INSERT OR IGNORE INTO informacoes_contato
   (id, telefone, email, horario, endereco)
VALUES
   (1, '(11) 99999-9999', 'contato@amigofiel.com',
    'Segunda a sábado, das 8h às 18h',
    'Rua Exemplo, 123 - Centro, Jundiaí - SP - Endereço fictício para demonstração');