import sqlite3

def criar_tabela():
    try:
        conexao = sqlite3.connect("filmes.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS filme (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            assistido BOOLEAN DEFAULT 0,                       
            avaliacao REAL
        )
        ''')
        
        conexao.commit()
        print("Tabela criada com sucesso!")
    except sqlite3.Error as erro:
        print(f"Erro ao criar tabela: {erro}")
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    criar_tabela()
