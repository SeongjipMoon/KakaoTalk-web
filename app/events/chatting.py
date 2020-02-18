from flask import session
from flask_socketio import send, emit, join_room, leave_room

from app import app, socketio
from app.routes.message import *


@socketio.on('joined', namespace='/chat')
def joined(data):
    url =  data['url']
    base = data['base'] + '/chat/room/'
    room = url.replace(base, '')
    
    join_room(room)

    nickName = session['profile_nickname']
    print(room + ', ' + nickName + ', 입장')
    emit('status', {'room': room, 'msg': str(nickName) + '님이 입장했습니다.'}, room=room)
    # db에 이름, 시간 저장


@socketio.on('left', namespace='/chat')
def left(message):
    room = 'apple'
    nickName = session['profile_nickname']
    print(room + ', ' + nickName + ', 퇴장')
    emit('status', {'msg': str(nickName) + '님이 나갔습니다.'}, room=room)
    # db에 이름, 시간 저장


@socketio.on('text', namespace='/chat')
def text(message):
    msg = message['msg']
    if msg != '\n' and msg != '':
        nickName = session.get('profile_nickname')
        room = message['room']
        msg = msg.replace('\n', '')
        
        print(room + ', ' + nickName + ', ' + msg)
        # send_me(msg)
        emit('message', {
            'name': nickName, 
            'msg': msg,
            'profile_img': session.get('profile_img')
            }, room=room)
        # db에 메세지, 이름, 시간 저장