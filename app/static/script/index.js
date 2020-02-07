require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('click', '.call-modal', function(e) {
            $('#modal-' + $(e.target).attr('modal-id')).modal('show');
        });
    });
});