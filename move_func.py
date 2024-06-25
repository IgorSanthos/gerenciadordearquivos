import shutil
from pathlib import Path
from datetime import datetime, timedelta
import os

#def
def move_files(df_filtrado):
    # # Obtém a data atual
    # data_atual = datetime.now()
    # # Calcula o primeiro dia do mês atual
    # primeiro_dia_mes_atual = data_atual.replace(day=1)
    # # Obtém o último dia do mês anterior subtraindo um dia do primeiro dia do mês atual
    # ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
    # # Formata o mês anterior e o ano atual como strings com duas casas decimais para o mês
    # mes_anterior = ultimo_dia_mes_anterior.strftime('%m')
    # ano_atual = ultimo_dia_mes_anterior.strftime('%Y')
    # # Cria a variável com mês e ano separados por underscore
    # dtCliente = f"{mes_anterior}_{ano_atual}"
    # # Verificar se o DataFrame filtrado está vazio
    #dtCliente = '/04_2024'

    if df_filtrado.empty:
        print("O DataFrame filtrado está vazio. Nenhuma ação a ser realizada.")
        return
    
    try:
        for index,row in df_filtrado.iterrows():
            #clienteJettax = Path(row['Origem'])
            diretorio_atual = os.path.abspath(os.path.dirname(__file__))
            caminho_absoluto_origem = Path(row['Origem'])
            caminho_relativo_origem = os.path.relpath(caminho_absoluto_origem, diretorio_atual)  # Transformando o caminho absoluto em um caminho relativo
            clienteJettax = Path(caminho_relativo_origem)  # Usando o caminho relativo


            caminho_absoluto = Path(row['Destino'])
            caminho_relativo = os.path.relpath(caminho_absoluto, diretorio_atual)# Transformando o caminho absoluto em um caminho relativo
            clienteDest = Path(caminho_relativo) # Usando o caminho relativo

            arquivos = {
                'enviada': list(clienteJettax.glob('enviada*')),
                'recebida': list(clienteJettax.glob('recebido*')),
                'nfts': list((clienteJettax / 'nfts').glob('nft*')),
                'guia': list((clienteJettax / 'guia').glob('guia*'))
            }

            destinos = {
                'nfs': [clienteDest / 'Arquivos XML/Serviços Prestados', clienteDest / 'Arquivos XML/Serviços Tomados'],
                'iss': clienteDest / 'Tributos'
            }

            for arquivo in arquivos['enviada']:
                shutil.copy(arquivo, destinos['nfs'][0])

            for arquivo in arquivos['recebida']:
                shutil.copy(arquivo, destinos['nfs'][1])

            for arquivo in arquivos['guia']:
                shutil.copy(arquivo, destinos['iss'])

            for arquivo in arquivos['nfts']:
                shutil.copy(arquivo, destinos['nfs'][1])

        print(destinos)#f"Arquivos movidos com sucesso.{clienteDest} ==== {clienteJettax}" )

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except PermissionError as e:
        print(f"Erro: Permissão negada - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
