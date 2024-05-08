import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
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
        print("Exluido!")

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
def add(dayCluster, clientName, origem, destino):
    try:
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

    except Exception as e:
        print("Erro: - ", e)


# Chamando funcao
#add(dayCluster, client_name, origem, destino)
#------------------------------------------------------------------------------ Seleção
def select():
    try:
        # Conectar ao banco de dados
        engine = create_engine('mysql://root:@localhost/cadastro')

        # Query SQL para selecionar todos os registros da tabela cliente
        query = "SELECT * FROM cliente"

        # Carregar os dados em um DataFrame do Pandas
        df = pd.read_sql(query, engine)
        return df

    except Exception as erro:
        print("Erro ao carregar dados do banco:", erro)