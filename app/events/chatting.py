from flask import session
from flask_socketio import send, emit, join_room, leave_room

from app import app, socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    print(joined)
    room = 'test'
    join_room(room)
    nickName = session['ninkName']
    emit('status', {'msg': str(nickName) + '님이 입장했습니다.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {
        'name': session.get('name'), 
        'msg':  message['msg']}, room=room)