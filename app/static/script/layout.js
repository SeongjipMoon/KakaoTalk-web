require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('click', '.link', function(e) {
            $(location).attr('href', '' + '/' + $(e.target).attr('menu'))
        });
    });
});