
from flask  import Flask, render_template
import sql_func as sql                                  # type: ignore
from flask import request                               # Importe o objeto request
import move_func as mv
app = Flask(__name__)                   # Obrigatorio - Ativação do framework flask 
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------   PAGINA 1 -  HOME
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method   ==  'POST':
        dataCluster = request.form.get('dayCluster')
        df = sql.select(dataCluster)
        df_filtrado = df[df['DataCluster'] == dataCluster]
        try:
            mv.move(df_filtrado)
            return ''''<script>
                    alert("Arquivos movidos com sucesso");
                    window.location.href = '/';
                    </script>''' 
        except Exception as e:
            print('Erro: ', e)

    return render_template('index.html')
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------  PAGINA 2 - SELEÇÃO DE CLIENTES
@app.route('/selecionar-cliente', methods=['POST', 'GET'])                               # Route -> e o que vem depois do nome do site por se eu colocar (/) a homepage
def clienteGeral():                                             # Funcao para traser o banco de dados    
    if request.method   ==  'POST':
        try:
            dataCluster = request.form.get('dayCluster')
            df = sql.select(dataCluster)                                # Tras a funcao do arquivo sql_func para a variavel df
            if df is not None:                                          # Se a variavel df conter algo atribua df a variavel html_table
                html_table = df.to_html()                            # muda o Pandas para html
            return render_template("pagina_2.html", table=html_table)   # Junta(Renderiza) a variavel do python para o html 
        except Exception as e:
            print('Erro: ', e)
            return "ocorreu um erro", 500
    return render_template("pagina_2.html")
#----------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------- PAGINA 3 - ADICIONAR NOVO  
@app.route('/adicionar-cliente', methods=['POST', 'GET'])

def adicionar():
    if request.method == 'POST':
        try:
            dayCluster  = request.form.get('dayCluster')    # vindo do Front End
            clientName  = request.form.get('clienteName')   # vindo do Front End
            sql.add(dayCluster, clientName)
            
            return ''''<script>
                    alert("Cliente adicionado com sucesso");
                    window.location.href = 'adicionar-cliente';
                    </script>'''
            
        except Exception as e:
            print('Erro *********', e)  # Se ocorrer um erro, você pode querer redirecionar o usuário para uma página de erro

    return render_template("pagina_3.html")
 
#------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------DELETE PAGINA 4

@app.route('/excluir', methods=['POST', 'GET'])
def selectDelete():
    if request.method == 'POST':
        action = request.form.get('action')  # Obtenha a ação do formulário
        
        if action == 'selectData':
            try:
                dataCluster = request.form.get('dayCluster')
                df = sql.select(dataCluster)
                if df is not None:
                    html_table = df.to_html()
                    return render_template("pagina_4.html", table=html_table)
                else:
                    return "Nenhum dado encontrado", 404
            except Exception as e:
                print('Erro: ', e)
                return "Ocorreu um erro", 500

        elif action == 'deleteClient':
            try:
                id_client = request.form.get('idClient')
                sql.excluir(id_client)
                return '''
                    <script>
                        alert("Cliente excluído com sucesso");
                        window.location.href = '/excluir';
                    </script>'''
            except Exception as e:
                print('Erro: ', e)
                return "Ocorreu um erro ao excluir o cliente", 500

    return render_template("pagina_4.html")

#---------------------------------  FIM ------------------------------------------------
#---------------------------------  FIM ------------------------------------------------------------------------
if __name__ == "__main__":              # Obrigatorio - Atualiza a pagina automaticamente
    app.run(debug=True)


# function.move()
#   excluir cliente  
