import requests
#import shutil
from pathlib import Path
#from datetime import datetime, timedelta
import os

def move_files(df_filtrado=None):
    if df_filtrado is None:
        return []
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
    
    url = 'http://localhost:5001/move'
    messages_list = []  # Inicializa a lista vazia para armazenar as mensagens
    
    try:
        for index,row in df_filtrado.iterrows():
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


        # Envio de Requisições para Movimentação de Arquivos
            for arquivo in arquivos['enviada']:
                #shutil.copy(arquivo, destinos['nfs'][0])
                data = {'source':str(arquivo), 'destination': str(destinos['nfs'][0])}
                response = requests.post(url, json=data)
                handle_response(response, messages_list)
                

            for arquivo in arquivos['recebida']:
                #shutil.copy(arquivo, destinos['nfs'][1])
                data = {'source': str(arquivo), 'destination': str(destinos['nfs'][1])}
                response = requests.post(url, json=data)
                handle_response(response, messages_list)


            for arquivo in arquivos['guia']:
                #shutil.copy(arquivo, destinos['iss'])
                data = {'source': str(arquivo), 'destination': str(destinos['iss'])}
                response = requests.post(url, json=data)
                handle_response(response, messages_list)


            for arquivo in arquivos['nfts']:
                #shutil.copy(arquivo, destinos['nfs'][1])
                data = {'source': str(arquivo), 'destination': str(destinos['nfs'][1])}
                response = requests.post(url, json=data)
                handle_response(response, messages_list)


        print(f"Arquivos copiados com sucesso.")
        return messages_list
    except FileNotFoundError as e:
        messages_list.append(f"Erro: Arquivo não encontrado - {e}")
    except PermissionError as e:
        messages_list.append(f"Erro: Permissão negada - {e}")
    except Exception as e:
        messages_list.append(f"Erro inesperado: {e}")
    return messages_list    

def handle_response(response, messages_list):
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            messages_list.append(f"Copiado com sucesso: {result['message']}")
        else:
            messages_list.append(f"Erro ao copiar: {result['message']}")
    else:
        messages_list.append(f"Erro na requisição: {response.status_code}")

     # print do nome do cliente

def save_messages_list_to_desktop(messages_list):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, 'messages_list.txt')

    with open(file_path, 'w') as file:
        for message in messages_list:
            file.write(f"{message}\n")

    print(f"Mensagens salvas com sucesso em {file_path}")