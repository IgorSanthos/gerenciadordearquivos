
import os
from flask  import Flask, render_template, redirect, url_for, request
from move_func import move_files
import pandas as pd
from bs4 import BeautifulSoup
import logging

# INICIO
app = Flask(__name__)

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# PAGINA 1 HOME
@app.route('/')
def index():        
    return render_template('index.html')


# FUNCAO MOVE
@app.route('/move', methods=['POST'])
def move():
    try:
        # Criação de caminho relativo
        index_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        #
        with open(index_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        #
        diacluster = request.form.get('comp_select')
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_=diacluster)
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:  # Verifica se há pelo menos duas colunas
                datacluster = cols[0].text.strip()
                nome = cols[1].text.strip()
                origem = cols[2].text.strip()
                destino = cols[3].text.strip()
                data.append([datacluster, nome, origem, destino])
        # Cria o DataFrame com a origem e destino selecionados
        df_filtrado = pd.DataFrame(data, columns=['DataCluster', 'Nome', 'Origem', 'Destino'])
        # Chamando a funcao Move
        move_files(df_filtrado)
        
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao mover arquivos: {e}", 500

# PAGINA 2 - SELEÇÃO DE CLIENTES
@app.route('/selecionar-cliente')
def clienteGeral():
    return render_template("pagina_2.html")


# PAGINA 3 - ADICIONAR NOVO  
@app.route('/adicionar-cliente')
def adicionar():
    return render_template("pagina_3.html")


# DELETE PAGINA 4
@app.route('/excluir')
def selectDelete():
    return render_template("pagina_4.html")


# FINAL 
if __name__ == "__main__":              
    app.run(debug=True)