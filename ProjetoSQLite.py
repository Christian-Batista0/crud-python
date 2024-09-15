#Christian da Silva Batista
#Pré-Projeto da aplicação CRUD
#cadastramento de alunos em uma instituição de ensino(faculdade ou escola)

#importação da biblioteca colorama (para cores de tabela e mensagens) || pip install colorama
from colorama import Fore, Style 
import os
import sqlite3
from contextlib import closing
from datetime import datetime
####INCIO FUNÇÕES####

def adicionarAluno (novoCpf):
    resultado = fetchBycriteria("cpf",(novoCpf,))
    if resultado:
        print(Fore.RED + "CPF já cadastrado no sistema" + Style.RESET_ALL)
        esperar()
    else:
        novoNome = input("digite o nome do aluno: ")
        dataNasc = input("digite a data de nascimento do aluno: ")
        dataFormat = datetime.strptime(dataNasc, "%d/%m/%Y").strftime("%Y-%m-%d")
        fetch_query('insert into alunos (nome,cpf,datanasc) values(?,?,?)',(novoNome,novoCpf,dataFormat,))
        resultado1 = fetchBycriteria('cpf',(novoCpf,))
        os.system('cls')
        print("aluno adicionado com sucesso")
        listarDados(resultado1)
        esperar()

def removerAluno (codigoId):
    resultado = fetchBycriteria("id",(codigoId,))
    if not resultado:
        print("id não encontrado")
    else:
        print(Fore.RED + "ATENÇÃO!!! o seguinte aluno será removido: " + Style.RESET_ALL)
        listarDados(resultado)
        confirm = input("continuar com a remoção? Digite sim ou aperte enter para cancelar e voltar ao menu: ").lower()
        if confirm == "sim":
            query = "delete from alunos where id = ?" 
            fetch_query(query,(codigoId,))
            print("removido com sucesso")
            esperar()

def alterarAluno(Id):
        resultado = fetchBycriteria("id",(codigoId,))
        if resultado:
            print(Fore.RED + "ATENÇÃO, o seguinte aluno será editado: " + Style.RESET_ALL)
            listarDados(resultado)
            opcAlterar = verificarInt("digite a opção a ser alterada\n1- nome\n2- data de nascimento\n:")
            if opcAlterar == 1:
                alterarNome = input("digite o novo nome: ")
                query = (f'update alunos set nome = ? where id = ?')
                params = ((alterarNome,Id,))
                fetch_query(query,params)
                alterado = True
            elif opcAlterar == 2: 
                alterarNasc = input("digite a nova data de nascimento: ")
                dataFormat = datetime.strptime(alterarNasc, "%d/%m/%Y").strftime("%Y-%m-%d")
                query = (f'update alunos set datanasc = ? where id = ?')
                params = ((dataFormat,Id,))
                fetch_query(query,params)
                alterado = True
            else: 
                print("opção inválida")
                esperar()
                alterado = None

            if alterado:   
                alterado = fetchBycriteria("id",(codigoId,)) 
                os.system('cls')
                print(Fore.BLUE + "alteração concluida com sucesso: " + Style.RESET_ALL)
                listarDados(alterado) #lista os dados após a alteração
                esperar()    
        else:
            print(f"não foi encontrado nenhum aluno com o ID: {codigoId}")
            esperar()

def listarDados(dados):
    #TABELA
    #linha superior
    cor_borda = Fore.GREEN
    cor_texto = Fore.WHITE

    print(cor_borda + "+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 17 + "+")
    #cabeçalho
    print(f"| {'ID':^3} | {'Nome':^30} | {'CPF':^15} | {'Data Nascimento':^12} |")
    #linha divisória
    print(cor_borda +"+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 17 + "+")
    #linha de dados
    for linha in dados:
        dataFormat = datetime.strptime(linha[3], "%Y-%m-%d").strftime("%d/%m/%Y") #usando a biblioteca datatime para transformar na data brasileira 
        print(f"| {cor_texto}{linha[0]:^3} | {cor_texto}{linha[1]:<30} | {cor_texto}{linha[2]:^15} | {cor_texto}{dataFormat:^15} |")
    #Linha inferior
    print(cor_borda +"+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 17 + "+")
    print(Style.RESET_ALL)
    

def imprimirDadosAluno(dados):
    cor_borda = Fore.GREEN
    cor_texto = Fore.WHITE

    #linha superior com a cor da borda
    print(cor_borda + "+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 14 + "+")

    # cabeçalho da tabela com a cor do texto
    print(cor_borda + f"| {cor_texto}{'ID':^3} | {cor_texto}{'Nome':^30} | {cor_texto}{'Data Nascimento':^15} | {cor_texto}{'CPF':^12} |")

    # linha divisóriacom a cor da borda
    print(cor_borda + "+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 14 + "+")

    # linha de dados com a cor do texto
    print(cor_borda + f"| {cor_texto}{dados[0]:^3} | {cor_texto}{dados[1]:<30} | {cor_texto}{dados[2]:^15} | {cor_texto}{dados[3]:^12} |")

    # linha inferiorcom a cor da borda
    print(cor_borda + "+" + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 14 + "+")
    print(Style.RESET_ALL)

def verificarInt(entrarInput, opc2 = None): #função loop para verificar a entrada de um numero inteiro por parte do usuario, apenas o retorno de um numero inteiro valido, encerrará o looping
    while True:
        entrada = input(entrarInput)
        if entrada == "000":
            return None
        try:
            numero = int(entrada)
            return numero
        except ValueError:
            print(Fore.RED + "por favor, digite um número inteiro." + Style.RESET_ALL)
            esperar()
            os.system('cls')

def esperar(): input("aperte enter para continuar") 
####FIM FUNÇÕES####


def fetchLista(query):
    with sqlite3.connect("educacad.db") as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(query)
            resultado = cursor.fetchall()
            listarDados(resultado)
            
def fetchSelect(query, params=None): #função para pesquisar o id no banco
      with sqlite3.connect("educacad.db") as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        
def fetch_query(query,params=None):
        with sqlite3.connect("educacad.db") as conexao:
            with closing(conexao.cursor()) as cursor:
                if params:
                    cursor.execute(query, params)
                    conexao.commit()
                else:
                    cursor.execute(query)
                conexao.commit()

def fetchBycriteria(criteria, params):
    if criteria == "name":   
        query = "SELECT * FROM alunos WHERE nome LIKE ?"
        params = ('%' + params[0] + '%',) # para fazer a pesquisa parcial, 
    elif criteria == "id":
        query = "SELECT * FROM alunos WHERE id = ?"
    elif criteria == "cpf":
        query = "SELECT * FROM alunos WHERE cpf = ?"
    else:
        raise ValueError("Critério de pesquisa inválido.")
    return fetchSelect(query, params,)

#### FIM TXT ####


while True:
    os.system('cls')
    logo = ('''
     ┏┏┓┳┓┳┳┏┓┏┓┏┓┏┓┳┓┓     
━━━━━┫┣ ┃┃┃┃┃ ┣┫┃ ┣┫┃┃┣━━━━━
     ┗┗┛┻┛┗┛┗┛┛┗┗┛┛┗┻┛┛     
''')
    cor = Fore.CYAN

    print(cor + logo,Style.RESET_ALL)
    print("1 - Ver lista completa\n2 - Pesquisar aluno\n3 - Adicionar aluno\n4 - Remover aluno\n5 - Editar aluno\n6 - Sair\n", Fore.YELLOW + "*** digite 000 (três zeros) para voltar ao menu ***\n" +Style.RESET_ALL)
    opc = verificarInt("Selecione a opção desejada\n:")
    os.system('cls')
    
    if opc is None:  # opcão de voltar
                continue  # Volta ao início do loop para exibir o menu novamente
    if opc == 6:
        print(cor + logo,Style.RESET_ALL)
        print("Saindo do programa...")
        #saveTxt(turmaA)
        break
    
    elif opc == 1:
                query = 'select * from alunos'
                resultados= fetchLista(query)
                esperar()

    ##### OPÇÕES ESOLHA 2 ######    
    elif opc == 2:
      
        opc2 = verificarInt("Digite o numero correspondente a sua pesquisa:\n1 - pesquisar nome\n2 - pesquisar CPF\n3 - pesquisar ID\n:") 
        if opc2 is None:  # opcão de voltar
                continue  # Volta ao início do loop para exibir o menu novamente
        if opc2 == 1:
            name = input("Digite o nome: ")
            if not name:
                continue
            resultado = fetchBycriteria("name",(name,))
            if resultado:
                listarDados(resultado)
                esperar()
            else:
                print(Fore.YELLOW + f"não foi encontrado nenhum aluno com o nome: {name} " + Style.RESET_ALL)
                esperar()


        elif opc2 == 2:
            cpf = verificarInt("Digite o cpf: ")
            if cpf is None:  
                continue  
            resultado = fetchBycriteria('cpf',(cpf,))
            if resultado:
                  listarDados(resultado) 
            else:
                print(Fore.YELLOW + f"não foi encontrado nenhum aluno com o CPF: {cpf} " + Style.RESET_ALL)
            esperar()

        elif opc2 == 3:
            codigoId = verificarInt("Digite o ID do aluno: ")
            if codigoId is None: 
                continue 
            resultado = fetchBycriteria("id",(codigoId,))
            if resultado:
                listarDados(resultado) 
                esperar()
            else:
                print(Fore.YELLOW + f"não foi encontrado nenhum aluno com o id: {codigoId} " + Style.RESET_ALL)
                esperar()

        else:
            print("opção invalida")
            esperar()

    elif opc == 3:
        novoCpf = verificarInt("Digite o CPF do novo aluno: ")
        if novoCpf is None:  
                continue  
        adicionarAluno(novoCpf)
    
    elif opc == 4:
        codigoId = verificarInt("digite o ID do aluno: ")
        if codigoId is None:  
                continue  
        removerAluno(codigoId)
        
    elif opc == 5:
        codigoId = verificarInt("Digite o ID do aluno para altera-lo: ")
        if codigoId is None:  
                continue
        alterarAluno(codigoId)
        
        
    else: 
        print(Fore.RED + "opção inválida" + Style.RESET_ALL)
        esperar()