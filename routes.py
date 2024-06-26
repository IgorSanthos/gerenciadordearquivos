
import os
from flask  import Flask, render_template, redirect, url_for, flash, request
import pandas as pd
from bs4 import BeautifulSoup
from move_func import move_files, save_messages_list_to_desktop


app = Flask(__name__)               # INICIO

app.secret_key = os.urandom(24)

# PAGINA 1 HOME
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório do arquivo atual

@app.route('/')
def index():
    if 'message' in request.args:
        flash(request.args['message'], request.args['message_type'])        
    return render_template('index.html')



# FUNCAO MOVE
@app.route('/move', methods=['POST'])
def move():
    try:

        index_path = os.path.join(BASE_DIR, 'templates', 'index.html')  # Criação de caminho relativo
        
        with open(index_path, 'r', encoding='utf-8') as file:   # Lê o conteúdo do arquivo index.html
            html_content = file.read()

        diacluster = request.form.get('comp_select')    # Obtém o valor do campo 'comp_select' do formulário POST
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_=diacluster)
        rows = table.find_all('tr')
        data = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:                          # Verifica se há pelo menos duas colunas
                datacluster = cols[0].text.strip()
                nome = cols[1].text.strip()
                origem = cols[2].text.strip()           # Origem vinda do HTML
                destino = cols[3].text.strip()          # Destino vindo do HTML
                data.append([datacluster, nome, origem, destino])
                
        # Cria o DataFrame com a origem e destino selecionados
        df_filtrado = pd.DataFrame(data, columns=['DataCluster', 'Nome', 'Origem', 'Destino'])

        # Chamando a funcao Move
        messages_list = move_files(df_filtrado)

        if not messages_list:
            flash("A lista de mensagens está vazia.", "error")
        else:
            save_messages_list_to_desktop(messages_list)
            flash("Lista de erros salvos", "success")
        
        return redirect(url_for('index', message="Lista de erros salvos no desktop !", message_type="success"))
        
    except Exception as e:
        flash(f"Erro ao mover arquivos: {str(e)}", "danger")
        return redirect(url_for('index', message=f"Erro ao mover arquivos: {str(e)}", message_type="danger"))


# PAGINA 2 - SELEÇÃO DE CLIENTES
@app.route('/selecionar-cliente')
def clienteGeral():
    return render_template("pagina_2.html")


# FINAL 
if __name__ == "__main__":              
    app.run(debug=True)