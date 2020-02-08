require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('click', '.link', function(e) {
            $(location).attr('href', '' + '/' + $(e.target).attr('menu'))
        });

        $(document).on('click', '.chatting', function(e) {
            $('#modal-' + '1-2').modal('show');
        });

        $(document).on('dblclick', '.profile_name', function(e) {
            $('#modal-' + '1-2').modal('show');
        });
    });
});