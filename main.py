import sqlite3

def conectar():
    return sqlite3.connect("filmes.db")

def criar_filme(titulo: str, genero: str, ano: int, assistido: bool = False, avaliacao: float = None):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO filme (titulo, genero, ano, assistido, avaliacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, genero, ano, assistido, avaliacao))
        conexao.commit()
        print("Filme adicionado com sucesso!")
    except Exception as erro:
        print(f"Erro ao adicionar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def deletar_filme(id_filme: int):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM filme WHERE id = ?', (id_filme,))
        conexao.commit()
        print("Filme deletado com sucesso!")
    except Exception as erro:
        print(f"Erro ao deletar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def buscar_filme(titulo: str):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM filme WHERE titulo LIKE ?', ('%' + titulo + '%',))
        filmes = cursor.fetchall()
        if filmes:
            for filme in filmes:
                print("====================================================================================================")
                print(f"""ID: {filme[0]}
Nome: {filme[1]}
Gênero: {filme[2]}
Ano: {filme[3]}
Assistido: {filme[4]}
Avaliação: {filme[5]}""")
        else:
            print("Nenhum filme encontrado com o título informado.")
    except Exception as erro:
        print(f"Erro ao buscar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def listar_filmes():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM filme')
        todos_filmes = cursor.fetchall()
        if todos_filmes:
            for filme in todos_filmes:
                assistido = "Sim" if filme[4] else "Não"
                print("====================================================================================================")
                print(f"""ID: {filme[0]}
Nome: {filme[1]}
Gênero: {filme[2]}
Ano: {filme[3]}
Assistido: {assistido}
Avaliação: {filme[5]}""")
        else:
            print("Nenhum filme encontrado.")
    except Exception as erro:
        print(f"Erro ao listar filmes: {erro}")
    finally:
        cursor.close()
        conexao.close()

def atualizar_dados_filme(id_filme: int, titulo: str = None, genero: str = None, ano: int = None, avaliacao: float = None, assistido: bool = None):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        campos = []
        valores = []

        if titulo is not None:
            campos.append('titulo = ?')
            valores.append(titulo)
        if genero is not None:
            campos.append('genero = ?')
            valores.append(genero)
        if ano is not None:
            campos.append('ano = ?')
            valores.append(ano)
        if avaliacao is not None:
            campos.append('avaliacao = ?')
            valores.append(avaliacao)
        if assistido is not None:
            campos.append('assistido = ?')
            valores.append(assistido)

        if campos:
            valores.append(id_filme)
            cursor.execute(f'UPDATE filme SET {", ".join(campos)} WHERE id = ?', valores)
            conexao.commit()
            print("Filme atualizado com sucesso!")
        else:
            print("Nenhuma alteração foi feita.")
    except Exception as erro:
        print(f"Erro ao atualizar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def marcar_como_assistido(id_filme: int):
    atualizar_dados_filme(id_filme, assistido=True)

def avaliar_filme(id_filme: int):
    while True:
        try:
            avaliacao = input("Digite a avaliação (0 a 5, ou deixe em branco para cancelar): ")
            if not avaliacao:
                print("Operação cancelada.")
                return
            avaliacao = float(avaliacao)
            if 0 <= avaliacao <= 5:
                atualizar_dados_filme(id_filme, avaliacao=avaliacao)
                print("Avaliação feita com sucesso!")
                break
            else:
                print("A avaliação deve ser de 0 a 5.")
        except ValueError:
            print("Valor inválido. Digite um número de 0 a 5.")

def obter_avaliacao_usuario():
    while True:
        try:
            avaliacao = input("Digite a avaliação (0 a 5, ou deixe em branco para não opinar): ").strip()
            if not avaliacao:
                return None
            avaliacao = float(avaliacao)
            if 0 <= avaliacao <= 5:
                return avaliacao
            else:
                print("A avaliação deve ser de 0 a 5.")
        except ValueError:
            print("Valor inválido. Digite um número de 0 a 5.")

def menu():
    while True:
        print("""
        Menu:
        [1].Adicionar filme
        [2].Listar filmes
        [3].Deletar filme
        [4].Atualizar dados do filme
        [5].Marcar filme como assistido
        [6].Avaliar filme
        [7].Buscar filme
        [8].Sair""")
        
        try:
            escolha = int(input("Digite sua escolha: "))
        except ValueError:
            print("Escolha inválida. Tente novamente.")
            continue

        if escolha == 1:
            print("Criar filme:")
            titulo = input("Título: ")
            genero = input("Gênero: ")
            try:
                ano = int(input("Ano: "))
            except ValueError:
                print("Ano inválido. Tente novamente.")
                continue
            assistido = input("Assistido? (s/n): ").strip().lower() == 's'
            avaliacao = obter_avaliacao_usuario()
            criar_filme(titulo, genero, ano, assistido, avaliacao)

        elif escolha == 2:
            listar_filmes()

        elif escolha == 3:
            try:
                id_filme = int(input("Digite o ID do filme a ser deletado: "))
                deletar_filme(id_filme)
            except ValueError:
                print("ID inválido. Tente novamente.")

        elif escolha == 4:
            try:
                id_filme = int(input("Digite o ID do filme que deseja atualizar: "))
                titulo = input("Novo título (deixe em branco para manter o mesmo): ") or None
                genero = input("Novo gênero (deixe em branco para manter o mesmo): ") or None
                ano_input = input("Novo ano (deixe em branco para manter o mesmo): ")
                ano = int(ano_input) if ano_input else None
                assistido = input("Assistido? (s/n, deixe em branco para manter o mesmo): ").strip().lower()
                assistido = True if assistido == "s" else None
                avaliacao_input = input("Avaliação (0 a 5, deixe em branco para manter o mesmo): ")
                avaliacao = float(avaliacao_input) if avaliacao_input else None
                if avaliacao is not None and (avaliacao < 0 or avaliacao > 5):
                    print("A avaliação deve ser entre 0 e 5. Tente novamente.")
                    continue
                atualizar_dados_filme(id_filme, titulo, genero, ano, avaliacao, assistido)
            except ValueError:
                print("ID inválido ou outro erro na entrada. Tente novamente.")

        elif escolha == 5:
            try:
                id_filme = int(input("Digite o ID do filme para marcar como assistido: "))
                marcar_como_assistido(id_filme)
            except ValueError:
                print("ID inválido. Tente novamente.")

        elif escolha == 6:
            try:
                id_filme = int(input("Digite o ID do filme para avaliar: "))
                avaliar_filme(id_filme)
            except ValueError:
                print("ID inválido. Tente novamente.")

        elif escolha == 7:
            titulo = input("Digite o título do filme para buscar: ")
            buscar_filme(titulo)

        elif escolha == 8:
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
