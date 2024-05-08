import shutil
from pathlib import Path
from datetime import datetime, timedelta
import sql_func as sql

# Leitura da planilha
df = sql.select()

# dateCluster = index.cluster

# Filtrando do DataFrame pela coluna 'DataCluster'
df_filtrado = df[df['DataCluster'] == '2024-04-02']

def move():    
    # Verificar se o DataFrame filtrado está vazio
    if df_filtrado.empty:
        print("O DataFrame filtrado está vazio. Nenhuma ação a ser realizada.")
        return
    
    try:
        for i in range(len(df_filtrado)):
            day = datetime.now().date()
            month = day - timedelta(days=day.day)
            dtCliente = month.strftime("%m_%Y")
            clienteJettax = Path(df_filtrado.at[i, 'Origem'])
            clienteDest = Path(df_filtrado.at[i, 'Destino']) / dtCliente

            client = [clienteJettax, clienteDest]
            
            arqEnv = list(client[0].glob('enviada*'))
            arqRec = list(client[0].glob('recebido*'))
            arqNfts = list((client[0] / 'nfts').glob('nft*'))
            arqGuia = list((client[0] / 'guia').glob('guia*'))

            destNfs = [client[1] / 'Arquivos XML/Serviços Prestados', client[1] / 'Arquivos XML/Serviços Tomados']
            destIss = client[1] / 'Tributos'

            for arquivo in arqEnv:
                shutil.copy(arquivo, destNfs[0])

            for arquivo in arqRec:
                shutil.copy(arquivo, destNfs[1])

            for arquivo in arqGuia:
                shutil.copy(arquivo, destIss)

            for arquivo in arqNfts:    
                shutil.copy(arquivo, destNfs[1])

            print("Arquivos movidos com sucesso.")

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except PermissionError as e:
        print(f"Erro: Permissão negada - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

move()
