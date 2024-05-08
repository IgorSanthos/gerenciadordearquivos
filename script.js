    //                      SELECIONAR CLIENTES  
    document.getElementById("ativarTabela").addEventListener("click", function() {
        var edit = document.getElementById("tabelaCliente");
        edit.style.display = "block";
        
    // Adiciona um console.log para verificar se a função está sendo chamada
        console.log("Função de evento acionada. Div 'tabelaCliente' exibida.");

    });

//                      ADICIONAR CLIENTE
    document.getElementById("adicionarCliente").addEventListener("click", function() {
        // Quando o botão for clicado, redireciona para a rota /adicionar-cliente com o parâmetro executar=true
        window.location.href = "/adicionar-cliente?executar=true";
    });

/*                     ADICIONAR CLIENTE
document.getElementById("adicionarCliente").addEventListener("click", function() {
    // Captura o valor dos campos do formulário
    var dayCluster  = document.getElementById("dayCluster").value;
    var clienteName = document.getElementById("clienteName").value;
    var origem      = document.getElementById("origem").value;
    var destino     = document.getElementById("destino").value;

    // Cria um objeto FormData e adiciona os valores dos campos
    var formData = new FormData();
    formData.append('dayCluster', dayCluster);
    formData.append('clienteName', clienteName);
    formData.append('origem', origem);
    formData.append('destino', destino);

    // Cria uma solicitação AJAX
    var xhr = new XMLHttpRequest();

    // Configura a solicitação para enviar os dados via método POST para a rota /adicionar-cliente
    xhr.open("GET", "/adicionar-cliente", true);

    // Define a função de retorno de chamada para lidar com a resposta do servidor
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // A resposta do servidor está pronta e foi bem-sucedida
            alert('Cliente adicionado com sucesso')
            console.log(xhr.responseText);
        }
    };
    // Envia os dados do formulário para o servidor
    xhr.send(formData);
});




**/