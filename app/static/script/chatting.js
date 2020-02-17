var socket;
    
$(document).ready(function(){                                
    var $comments = $('.comments');
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        var message = data.msg;

        var $div = $(`<div class="ui log label"></div>`)
            .text(message)
        
        $comments.append($div);
    });
    socket.on('message', function(data) {
        var name = data.name;
        var message = data.msg;
        var Now = new Date();

        if (Now.getHours > 12) {
            var date = '오후 ' + Now.getHours()-12 
                + ':' + Now.getMinutes();
        }
        else {
            var date = '오전 ' + Now.getHours()
                + ':' + Now.getMinutes();
        }

        var $name = $('<a class="author">').append(name);
        var $date = $('<span class="date">').append(date);
        var $metadata = $('<div class="metadata">').append($date);
        var $name_date = $('<div>').append($name, $metadata);
        
        var $text = $('<div class="ui left pointing label text">')
            .append(message);

        
        var $content = $('<div class="content">')
            .append($name_date, $text);
        var $image = $(`
            <a class="avatar">
                <img class="ui circular image" src="/static/images/default.png">
            </a>
        `);

        var $comment = $(`
            <div class="comment">
        `).append($image, $content);                    
        
        $comments.append($comment);
        $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
    });

    $('#submit').click(function() {
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text});
    });

    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
            $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
        }
    });

    $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        window.location.href = "/";
    });
}