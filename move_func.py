import shutil
from pathlib import Path
import os

def move_files(df_filtrado):
    if df_filtrado.empty:
        print("O DataFrame filtrado está vazio. Nenhuma ação a ser realizada.")
        return

    try:
        for index, row in df_filtrado.iterrows():
            # Obtendo o diretório atual
            diretorio_atual = Path(__file__).parent.resolve()

            # Caminho de origem e destino usando pathlib
            caminho_absoluto_origem = Path(row['Origem']).resolve()
            caminho_absoluto_destino = Path(row['Destino']).resolve()

            # Validando e ajustando os caminhos
            if not caminho_absoluto_origem.is_absolute():
                clienteJettax = (diretorio_atual / caminho_absoluto_origem).resolve()
            else:
                clienteJettax = caminho_absoluto_origem

            if not caminho_absoluto_destino.is_absolute():
                clienteDest = (diretorio_atual / caminho_absoluto_destino).resolve()
            else:
                clienteDest = caminho_absoluto_destino

            # Arquivos a serem movidos
            arquivos = {
                'enviada': list(clienteJettax.glob('enviada*')),
                'recebida': list(clienteJettax.glob('recebido*')),
                'nfts': list((clienteJettax / 'nfts').glob('nft*')),
                'guia': list((clienteJettax / 'guia').glob('guia*'))
            }

            # Destinos para os arquivos
            destinos = {
                'nfs': [clienteDest / 'Arquivos XML/Serviços Prestados', clienteDest / 'Arquivos XML/Serviços Tomados'],
                'iss': clienteDest / 'Tributos'
            }

            # Copiando os arquivos para os destinos
            for arquivo in arquivos['enviada']:
                shutil.copy(arquivo, destinos['nfs'][0])

            for arquivo in arquivos['recebida']:
                shutil.copy(arquivo, destinos['nfs'][1])

            for arquivo in arquivos['guia']:
                shutil.copy(arquivo, destinos['iss'])

            for arquivo in arquivos['nfts']:
                shutil.copy(arquivo, destinos['nfs'][1])

        print(f"Arquivos movidos com sucesso. {destinos}")

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except PermissionError as e:
        print(f"Erro: Permissão negada - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
