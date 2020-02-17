from flask import session
from flask_socketio import send, emit, join_room, leave_room

from app import app, socketio
from app.routes.message import *


@socketio.on('joined', namespace='/chat')
def joined(data):
    print(data)
    room = 'apple'
    join_room(room)
    nickName = session['profile_nickname']
    print(nickName + '님이 입장했습니다.')
    emit('status', {'msg': str(nickName) + '님이 입장했습니다.'}, room=room)
    # db에 이름, 시간 저장


@socketio.on('left', namespace='/chat')
def left(message):
    print('leave')
    pass
    # db에 이름, 시간 저장


@socketio.on('text', namespace='/chat')
def text(message):
    msg = message['msg']
    if msg != '\n' and msg != '':
        # send_me(msg)
        room = message['room']
        
        emit('message', {
            'name': session.get('profile_nickname'), 
            'msg': msg,
            'profile_img': session.get('profile_img')
            }, room=room)