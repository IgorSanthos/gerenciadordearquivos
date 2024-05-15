import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import filedialog
# #   IMPUT
# id_client   =   20
# dayCluster  =   '2024-04-03'                                                        # vindo do Front End
# client_name =   'CLIENTE21'                                                         # vindo do Front End
# origem      =   'C:\\Users\\Igor\\Desktop\\Jettax\\geral\\dia3\\Cliente_jettax21'   # vindo do Front End
# destino     =   'C:\\Users\\Igor\\Desktop\\Cliente\\Cliente21'                      # vindo do Front End   
# # -----------------------------------------------------------------------------------------Excluir
def excluir(id_client):
    # Conectar ao banco de dados
    conexao = mysql.connector.connect(
        host     = "127.0.0.1",
        user     = "root",
        password = "",
        database = "cadastro"
    )

#   Verificar se a conexão foi bem-sucedida
    if conexao.is_connected():
        print('conexão bem-sucedida  ', id_client)

#   Conexao do banco
    cursor  = conexao.cursor()

#   variaveis de exclusao
    delete_cliente  =   "DELETE FROM cliente WHERE id = %s"    

# executar o comando
    cursor.execute(delete_cliente, (id_client,))

    #FINAL
    conexao.commit()
    cursor.close()
    conexao.close()


# # ----------------------------------------------------------------------------------------- Adicionar
def add(dayCluster, clientName):
    root = tk.Tk()
    root.iconbitmap(r'C:\Users\Igor\Desktop\Gerenciador\app\static\img\icon.ico')       # Definir o ícone personalizado
    root.withdraw()                                                                     # Ocultar a janela principal
    try:
        diretorioOrigem = filedialog.askdirectory(
            parent = root,
            title = "Selecionar diretorio de origem (Jettax)")

        diretorioDestino = filedialog.askdirectory(
            parent = root,
            title = "Selecionar diretorio de Destino (Pasta Cliente)")
        
        if diretorioOrigem and diretorioDestino:
            print("Origem:", diretorioOrigem,"  /   Destino:", diretorioDestino )

            origem = diretorioOrigem
            destino = diretorioDestino
            # Botão para selecionar diretório
            btn_selecionar = tk.Button(text="Selecionar Diretório")
            btn_selecionar.pack(padx=10, pady=5)

            # Conectar ao banco de dados
            conexao =   mysql.connector.connect(
                host        =   "127.0.0.1",
                user        =   "root",
                password    =   "",
                database    =   "cadastro"
            )
            
            if conexao.is_connected():
                    print("Conexão bem-sucedida!")
            #   Conexao do banco
            cursor  = conexao.cursor()
        
            add_cliente = """INSERT INTO cliente (DataCluster, Nome, Origem, Destino)
                            VALUES (%s, %s, %s, %s)"""
            
            # FINAL 
            cursor.execute(add_cliente, (dayCluster, clientName, origem, destino))
            conexao.commit()

            # Verifica se a inserção foi bem-sucedida
            if cursor.rowcount > 0:                 # cursor.rowcount e uma propriedade 
                print("Cliente adicionado com Sucesso!")
            else:
                print("Nenhuma Cliente inserido.")

            cursor.close()
            conexao.close()
        else: print("Diretorio não selecionado")
    except Exception as e:
        print("Erro: - ", e)
# Chamando funcao
#add(dayCluster, client_name, origem, destino)
#------------------------------------------------------------------------------ Seleção
def select(datacluster):
    try:
        # Conectar ao banco de dados
        engine = create_engine('mysql://root:@localhost/cadastro')

        # Query SQL para selecionar todos os registros da tabela cliente
        query = "SELECT * FROM cliente WHERE DataCluster = %s"

        # Carregar os dados em um DataFrame do Pandas
        df = pd.read_sql(query, engine, params=[(datacluster,)])
        return df

    except Exception as erro:
        print("Erro ao carregar dados do banco:", erro)

#------------------------------------------------------------------------------ Diretorio

def seleciona_diretorio(origem):
    diretorio = filedialog.askdirectory()
    if diretorio:
        origem = diretorio
        print("Diretório selecionado:", origem)
        
        # Faça o que quiser com o diretório selecionado
    else: print("Diretorio não selecionado")
    
    # Botão para selecionar diretório
    btn_selecionar = tk.Button(text="Selecionar Diretório", command=seleciona_diretorio)
    btn_selecionar.pack(padx=10, pady=5)

    # Executa a interface gráfica