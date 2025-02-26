import sqlite3

def conectar():
    return sqlite3.connect("filmes.db")

def criar_filme(titulo: str, genero: str, ano: int, assistido: bool = False, avaliacao: float = None):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO filme (titulo, genero, ano, assistido,avaliacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, genero, ano, assistido,avaliacao))
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
        for filme in filmes:
            print("====================================================================================================")
            print(f"""ID: {filme[0]}
            Nome: {filme[1]}
            Gênero: {filme[2]}
            Ano: {filme[3]}
            Assistido: {filme[4]}
            Avaliação: {filme[5]}""")
    except Exception as erro:
        print(f"Erro ao buscar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def listar_filmes():
    rassistido = ""
    try:
        conexao =conectar()
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT
            *
        FROM
            filme''')
        todos_filmes = cursor.fetchall()
        for filme in todos_filmes:
            print("====================================================================================================")
            if filme[4] == 1.0:
                rassistido = "Assistido = s"
            else:
                rassistido = "Assistido = n"
            print(f"""ID: {filme[0]}
Nome: {filme[1]}
Gênero: {filme[2]}
Ano: {filme[3]}
{rassistido}
Avaliação: {filme[5]}""")
    except Exception as erro:
        print(f"Erro ao listar filmes: {erro}")
    finally:
        conexao.commit()
        cursor.close()

def atualizar_dados_filme(id_filme: int, titulo: str = None, genero: str = None, ano: int = None, avaliacao: float = None, assistido: bool = None):
    try:
        conexao =conectar()
        cursor = conexao.cursor()
        campos=[]
        valores=[]
        if titulo is not None:
            campos.append('titulo = ?')
            valores.append(titulo)
        if genero is not None:
            campos.append("genero = ?")
            valores.append(genero)
        if ano is not None:
            campos.append("ano = ?")
            valores.append(ano)
        if avaliacao is not None:
            campos.append("avaliacao = ?")
            valores.append(avaliacao)
        if assistido is not None:
            campos.append("assistido = ?")
            valores.append(assistido)

        if campos:
            valores.append(id_filme)
            cursor.execute(f'''
            UPDATE filme SET {','.join(campos)} WHERE id = ?
            ''', valores)
            conexao.commit()
            print("Filme adicionado com sucesso!")
        else: 
            print("Nenhuma ação foi feita")

    except Exception as erro:
        print(f"Erro ao atualizar filme: {erro}")
    finally:
        cursor.close()
        conexao.close()

def marcar_como_assistido(id_filme:int):
    atualizar_dados_filme(id_filme,assistido=True)

def avaliar_filme(id_filme:int):
    while True:
        try:
            avaliacao =input("Digite a avaliação (0 a 5, ou deixe em branco para cancelar):")
            if not avaliacao:
                print("Operação cancelada.")
                return
            avaliacao = float(avaliacao)
            if 0 <= avaliacao <= 5:        
                atualizar_dados_filme(id_filme,avaliacao=avaliacao)
                print("Avaliação feita com sucesso!")
                break
            else:
                print("A avaliação deve ser de 0 a 5.")
        except ValueError:
            print("Valor invalido. Digite um número de 0 a 5.")

while True:
    print("""
    Menu:
    [1].Adicionar filme
    [2].Listar filme
    [3].Deletar filme
    [4].Atualizar dados do filme
    [5].Marcar filme como assistido
    [6].Avaliar filme
    [7].Buscar filme
    [8].Sair""")
    
    escolha = int(input("Digite sua escolha:"))

    match escolha:
        case 1:
            print("==================================================================================")
            print("Criar filme:")
            try:
                titulo = input("Titulo: ")
            except ValueError:
                print("Valor invalido, tente novamente.")
                titulo = input("Titulo: ")
            try:
                genero = input("Gênero: ")
            except ValueError:
                print("Valor invalido, tente novamente.")
                genero = input("Gênero: ")
            try:
                ano = int(input("Ano: "))
            except ValueError:
                print("Valor invalido. Digite o ano")
                ano = int(input("Ano: "))
            try:
                assistido = str(input("Assistido? s/n (deixe em branco para manter o mesmo): ")).strip().lower()
                assistido = True if assistido == "s" else False 
            except ValueError:
                print("Valor invalido")
                assistido = str(input("Assistido? s/n (deixe em branco para manter o mesmo): ")).strip().lower()

            avaliacao =input("Digite a avaliação (0 a 5, ou deixe em branco para não opnar):")
            if avaliacao:
                try:
                    avaliacao = float(avaliacao)
                    if not avaliacao:
                        print("Operação cancelada.")
                        avaliacao = None
                    avaliacao = float(avaliacao)
                    if 0 <= avaliacao <= 5:        
                        atualizar_dados_filme(id_filme,avaliacao=avaliacao)
                        print("Avaliação feita com sucesso!")
                        break
                    else:
                        print("A avaliação deve ser de 0 a 5.")
                except ValueError:
                    print("Valor invalido. Digite um número de 0 a 5.")
                    avaliacao = None
            else: 
                avaliacao = None
            criar_filme(titulo,genero,ano,assistido,avaliacao)

        case 2:
            print("==================================================================================")
            print("Mostrar filme:")
            listar_filmes()
        
        case 3:
            print("==================================================================================")
            print("Deletar:")
            id_filme = input("Digite o id do filme:")
            deletar_filme(id_filme)
            print("...")
            print("Deletado com sucesso!")
        
        case 4:
            print("==================================================================================")
            print("Atualizar:")
            id_do_filme = int(input("Digite o ip do filme que deseja atualizar:"))
            titulo = input("Titulo(deixe em branco para manter o mesmo): ") or None
            genero = input("Gênero(deixe em branco para manter o mesmo): ") or None
            ano = int(input("Ano(deixe em branco para manter o mesmo): ")) or None
            ano = int(ano) if ano else None
            assistido = input("Assistido? s/n (deixe em branco para manter o mesmo): ").strip().lower()
            assistido = True if assistido == "s" else None
            try:
                avaliacao = float(input("Avaliação (0 a 5)(deixe em branco para manter o mesmo): ")) or None
            except ValueError:
                print("Valor invalido. Deve ser um número de 0 a 5!")
                continue
            atualizar_dados_filme(id_filme, titulo, genero, ano, avaliacao, assistido)
            print("...")
            print("Atualizado com sucesso!")
        case 5:
            print("==================================================================================")
            print("Marcar como lido")
            id_filme = int(input("Digite o id do filme:"))
            marcar_como_assistido(id_filme)        
            print("...")
            print("Marcado com sucesso!")
        case 6:
            print("==================================================================================")
            print("Avaliar:")
            try:
                id_filme = int(input("Digite o ID do filme: "))
                avaliar_filme(id_filme)
            except ValueError:
                print("ID inválido.")
        case 7: 
            print("==================================================================================")
            print("Buscando")
            titulo = input("Digite o título do filme: ")
            buscar_filme(titulo)
        case 8:
            print("==================================================================================")
            print("Saindo...")
        case _:
            print("Opção invalida.")

    if __name__ == "__main__":
        conectar()

