require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('click', '.link', function(e) {
            $(location).attr('href', 'http://localhost:8080/' + $(e.target).attr('menu'))
        });
    });
});