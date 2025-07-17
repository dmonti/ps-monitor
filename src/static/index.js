$(function() {
    $.getJSON('/api/info')
        .done(function(data) {
            let html = '<table class="table table-bordered table-striped mt-2">';
            html += '<thead><tr class="table-primary"><th colspan="2" class="text-center">OS</th></tr></thead><tbody>';
            html += `<tr><td>Nome</td><td>${data.os.name}</td></tr>`;
            html += '<tr class="table-primary"><th colspan="2" class="text-center">Platform</th></tr>';
            $.each(data.platform, function(key, value) {
                html += `<tr><td>${key.charAt(0).toUpperCase() + key.slice(1)}</td><td>${value}</td></tr>`;
            });
            html += '</tbody></table>';
            $('#info').html(html);
        })
        .fail(function() {
            $('#info').html('<div class="alert alert-danger text-center">Erro ao carregar informações do sistema.</div>');
        });
});
