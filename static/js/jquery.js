//                      CALENDARIO


$(function() {
    $("#dayCluster").datepicker({
        dayNamesMin:   ['D','S','T','Q','Q','S','S','D'],
        monthNames:    ['Janeiro','Fevereiro','Março',
                        'Abril','Maio','Junho','Julho',
                        'Agosto','Setembro','Outubro',
                        'Novembro','Dezembro'],                 
        dateFormat:     "dd-mm-yy",
        showOn:         "button",
        buttonImage:    buttonImageURL,
        buttonImageOnly:true
    });
});

