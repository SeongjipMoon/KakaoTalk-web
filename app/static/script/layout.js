require(['/static/config.js'], function () {
    require(['jquery', 'semantic'], function ($, Semantic) {
        $(document).on('dblclick', '.profile .name', function(e) {
            var my_id = $(e.target).attr('id');
            $(location).attr('href', '' + '/chat/' + my_id);
        });

        $(document).on('click', '.header .comment.icon', function(e) {
            var my_id = $(e.target).attr('id');
            $(location).attr('href', '' + '/chat/' + my_id);
        });
    });
});