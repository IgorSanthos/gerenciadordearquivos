
from flask  import Flask, render_template, redirect, url_for
from move_func import move_files
import pandas as pd
from bs4 import BeautifulSoup


app = Flask(__name__)                   # Obrigatorio - Ativação do framework flask 
#----------------------------------------
@app.route('/')
def index():        
    return render_template('index.html')

# ---------------------------------------------

@app.route('/move', methods=['POST'])
def move():


    with open('C:\\Users\\Igor\\gerenciadordearquivos\\templates\\index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:  #Verifica se há pelo menos duas colunas
            datacluster = cols[0].text.strip()
            nome = cols[1].text.strip()
            origem = cols[2].text.strip()
            destino = cols[3].text.strip()
            data.append([datacluster, nome, origem, destino])
    #Cria o DataFrame com a origem e destino selecionados
    df_filtrado = pd.DataFrame(data, columns=['DataCluster', 'Nome', 'Origem', 'Destino'])


    # Chamando a funcao Move
    move_files(df_filtrado)
    return redirect(url_for('index'))

# #----------------------------------------  PAGINA 2 - SELEÇÃO DE CLIENTES
@app.route('/selecionar-cliente')                               # Route -> e o que vem depois do nome do site por se eu colocar (/) a homepage
def clienteGeral():
    return render_template("pagina_2.html")

# #---------------------------------------------- PAGINA 3 - ADICIONAR NOVO  
@app.route('/adicionar-cliente')

def adicionar():
    return render_template("pagina_3.html")
# #-----------------------------------------------------------DELETE PAGINA 4

@app.route('/excluir')
def selectDelete():
    return render_template("pagina_4.html")

# Obrigatorio - Atualiza a pagina 
if __name__ == "__main__":              
    app.run(debug=True)