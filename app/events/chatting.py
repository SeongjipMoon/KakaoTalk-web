from flask import session
from flask_socketio import send, emit, join_room, leave_room
from datetime import datetime

from app import app, socketio, mongo
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

            users = list()

            for user in room['users']:
                if user['id'] != session['id']:
                    users.append({
                        'id': user['id'], 
                        'nickname': user['nickname']
                    })

            data = {
                'content': msg,
                'room_name': room['name'],
                'sender': {
                    'id': session['id'], 
                    'nickname': session['nickname']
                },
                'receviers': users,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            mongo.db.messages.insert(data)
            mee = mongo.db.messages.find_one(data)
            mongo.db.rooms.update_one(
                {'name' : room['name']}, 
                {'$push': {'messages': mee}}
            )
            
            if room['group'] == False:
                send_me(msg)
            else:
                send_friend(room['users'], msg)