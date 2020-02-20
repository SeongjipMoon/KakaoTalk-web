from flask import session
from flask_socketio import send, emit, join_room, leave_room

from app import app, socketio
from app.routes.message import *


def get_room_name(data):
    url =  data['url']
    base = data['base'] + '/chat/room/'
    room = url.replace(base, '')
    
    return room


@socketio.on('joined', namespace='/chat')
def joined(data):
    room = get_room_name(data)
    
    join_room(room)

    nickName = session['nickname']
    print(room + ', ' + nickName + ',+ 입장했습니다.')
    emit('status', {'room': room, 'msg': str(nickName) + '님이 입장했습니다.'}, room=room)
    # db에 이름, 시간 저장


@socketio.on('left', namespace='/chat')
def left(data):
    nickName = session['nickname']
    room = get_room_name(data)

    print(room + ', ' + nickName + '- 퇴장했습니다.')
    emit('status', {'room': room, 'msg': str(nickName) + '님이 나갔습니다.'}, room=room)
    # db에 이름, 시간 저장


@socketio.on('text', namespace='/chat')
def text(message):
    if 'msg' in message:
        msg = message['msg']
        if msg != '\n' and msg != '':
            nickName = session['nickname']
            room = message['room']
            msg = msg.replace('\n', '')
            
            print(room + ', ' + nickName + ', ' + msg)
            emit('message', {
                'name': nickName, 
                'msg': msg,
                'profile_image': session['profile_image']
                }, room=room)
            
            name = room.replace('http://katalk.junghub.kr/chat/room/', '')
            room = mongo.db.rooms.find_one({'name': name})
            
            if room['group'] == False:
                send_me(msg)
            else:
                send_friend(room['users'], msg)