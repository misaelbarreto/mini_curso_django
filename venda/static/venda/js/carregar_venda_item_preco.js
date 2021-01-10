// (function($) {
//     $(document).on('formset:added', function(event, $row, formsetName) {
//         if (formsetName == 'vendaitem_set') {
//             // Do something
//             alert('Opa')
//         }
//     });

//     $(document).on('formset:removed', function(event, $row, formsetName) {
//         // Row removed
//     });
// })(django.jQuery);



$(document).ready(function () {
    $(".module").delegate("[id$=-produto]", "change", function () {
        var row = $(this).attr("id").split('vendaitem_set-')[1].split("-produto")[0];
        var produto_id = $(this).val();
        console.info(row);
        console.info(produto_id);

        $.ajax({
            url: '/venda/load_preco_produto/',
            data: {
                'produto_id': produto_id
            },
            success: function (data) {
                //alert(data.preco)
                //alert("vendaitem_set-" + row + "-preco")
                $("#id_vendaitem_set-" + row + "-preco").val(data.preco)
            }
        });


        // var json_url = "/admin/cmdb/switch_ports/" + switch_id + "/"
        // $("#vendaitem_set-" + row + "-Port").html("");
        // $.post("/admin/cmdb/switch_ports/" + switch_id + "/", { "func": "getNameAndTime" },
        //     function (data) {
        //         for (var i = 0; i < data.length; i++) {
        //             var onePort = "<option value=\"" + data[i].pk + "\">" + data[i].fields.PortNum + "</option>";
        //             $("#vendaitem_set-" + row + "-Port").append(onePort);
        //         }
        //     }, "json");
    });
});

