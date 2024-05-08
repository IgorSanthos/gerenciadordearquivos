
from flask  import Flask, render_template
import sql_func as sql                                  # type: ignore
from flask import request  # Importe o objeto request

app = Flask(__name__)                   # Obrigatorio - Ativação do framework flask 

#----------------------------------------   PAGINA 1 -  HOME
@app.route('/')
def index():
    return render_template('index.html')

#----------------------------------------   PAGINA 2 - SELEÇÃO DE CLIENTES
@app.route('/selecionar-cliente')              # Route -> e o que vem depois do nome do site por se eu colocar (/) sera sua homepage ex (https://www.youtube.com), para outra pagina se colocar (/feed/history/) apara acessar https://www.youtube.com/feed/history
def clienteGeral():                                             # Funcao para traser o banco de dados
    df = sql.select()                                           # Tras a funcao do arquivo sql_func para a variavel df
    if df is not None:                                          # Se a variavel df conter algo atribua df a variavel html_table
       html_table   =   df.to_html()                            # muda o Pandas para html
    else:                                                       # Se nao, mostrar mensagem.
        html_table  =   "<p>Nenhum dado disponível.</p>"        # mensagem    
    return render_template("pagina_2.html", table=html_table)   # Junta(Renderiza) a variavel do python para o html 


# #---------------------------------------------- PAGINA 3 - ADICIONAR NOVO   --------------------------------------------------------------------

@app.route('/adicionar-cliente', methods=['POST'])

def adicionar():
        if request.method == 'POST':
            try:
                dayCluster  = request.form.get('dayCluster')    # vindo do Front End
                clientName  = request.form.get('clienteName')              # vindo do Front End
                origem      = request.form.get('origem')              # vindo do Front End
                destino     = request.form.get('destino')              # vindo do Front End 
                sql.add(dayCluster, clientName, origem, destino)
            except Exception as e:
                print  ('Erro *********', e)
        return render_template("pagina_3.html")


























#---------------------------------  FIM ------------------------
if __name__ == "__main__":              # Obrigatorio - Atualiza a pagina automaticamente
    app.run(debug=True)


# function.move()
#   excluir cliente  
