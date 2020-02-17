from flask import session
from flask_socketio import send, emit, join_room, leave_room

from app import app, socketio
from app.routes.message import *


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = 'test'
    join_room(room)
    nickName = session['nickName']
    print(nickName + '님이 입장했습니다.')
    emit('status', {'msg': str(nickName) + '님이 입장했습니다.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    if message['msg'] != '\n':
        msg = message['msg']

        send_me(msg)
        room = session.get('room')
        emit('message', {
            'name': session.get('nickName'), 
            'msg': msg}, room=room)