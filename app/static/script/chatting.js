var socket;
var room_name;

$(document).ready(function(){   
    var $comments = $('.comments');
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    
    socket.on('connect', function() {
        socket.emit('joined', {
            url: document.URL, 
            base: 'http://' + document.domain + ':' + location.port, 
            time: new Date()
        });
    });

    socket.on('status', function(data) {
        var message = data.msg;
        room_name = data.room;

        var $div = $(`<div class="ui log label"></div>`)
            .text(message)
        
        $comments.append($div);
        $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
    });

    socket.on('message', function(data) {
        var nickName = $("#nickName").text();
        nickName = nickName.replace(/ /gi, '');
        nickName = nickName.replace(/\n/gi, '');

        var name = data.name;
        var profile_image = data.profile_image;
        var message = data.msg;

        var Now = new Date();
        var date = Now.getHours() + ':' + Now.getMinutes();

        var $name = $('<a class="author">').append(name);
        var $date = $('<span class="date">').append(date);
        var $metadata = $('<div class="metadata" style="margin-right: 10px;">').append($date);
        var $name_date = $('<div>').append($name, $metadata);
        
        if (nickName != name) {
            var $text = $('<div class="ui left pointing label text">')
                .append(message);
        
            var $content = $('<div class="content">')
                .append($name_date, $text);

            if (profile_image != '') {
                var $image = $(`<a class="avatar">`).append(
                    `<img class="ui circular image" src=` + profile_image + `>`
                );
            }
            else {
                var $image = $(`<a class="avatar">`).append(
                    `<img class="ui circular image" src=` + '../../static/images/default.png' + `>`
                );
            }

            var $comment = $(`
                <div class="comment">
            `).append($image, $content);
        }
        else {
            var $text = $('<div class="ui right pointing label text" style="background-color: #ffee52">')
                .append(message);
    
            var $content = $('<div class="content">')
                .append($metadata, $text);

            var $comment = $(`
                <div class="comment" style="text-align: right; margin-right: 20px;">
            `).append($content);
        }

        $comments.append($comment);
        $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
    });

    $('#submit').click(function() {
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text, room: room_name});
        $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
    });

    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text, room: room_name});
            $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
        }
    });

    $('.scrolling').scrollTop($('.scrolling')[0].scrollHeight);
});

function leave_room() {
    socket.emit('left', {
        url: document.URL, 
        base: 'http://' + document.domain + ':' + location.port
    }, 
    function() {
        socket.disconnect();
        window.location.href = "/";
    });
}