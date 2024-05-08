//                      CALENDARIO


$(function() {
    $("#dayCluster").datepicker({
        dayNamesMin:    ['D','S','T','Q','Q','S','S','D'],
        monthNames:     ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        dateFormat:     "dd-dd-yy",
        showOn:         "button",
        buttonImage:    buttonImageURL,
        buttonImageOnly: true,
        onSelect: function(dateText, inst) {
            $.ajax({
                url:        '/selecionar-cliente',
                type:       'GET',
                data:       {data: dateText},
                success:    function(response) {
                    alert('Data enviada com sucesso');
                },
                error: function(error) {
                    alert('Erro ao enviar data' + error);
                }
            });
        }
    });
});

