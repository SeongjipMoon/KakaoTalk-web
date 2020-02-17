require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('click', '.link', function(e) {
            $(location).attr('href', '' + '/' + $(e.target).attr('menu'))
        });

        $(document).on('click', '.chatting', function(e) {
            $('#modal-' + '1-2').modal('show');
        });


        $(document).on('dblclick', '.profile .name', function(e) {
            $(location).attr('href', '' + '/chat')
        });
        $(document).on('click', '.buttons', function(e) {
            $('.katalk.input').show();
            $('#modal-1').modal('hide');
        });
        $(document).on('click', '.close.icon', function(e) {
            $('.katalk.input').hide();
            
        });

    });
});