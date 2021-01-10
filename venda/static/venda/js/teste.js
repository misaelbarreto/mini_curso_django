$(document).ready(function () {
    // alert('Teste Opa');

    $("#id_produto").change(function () {
        $.ajax({
            url: '/venda/load_preco_produto/',
            data: {
                'produto_id': $(this).val()
            },
            success: function (data) {
                $('#id_preco').val(data.preco)
            }
        });

    });
});

