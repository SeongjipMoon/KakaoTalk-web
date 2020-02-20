from flask import render_template, url_for, redirect, abort
from datetime import datetime

from app import app, mongo
from app.tools import *
from app.constants import *
from app.routes.user import *


def make_date():
    week = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    now = datetime.now()
    date = str(now.year) + '년 ' + str(now.month) + \
        '월 ' + str(now.day) + '일 ' + \
        week[now.weekday()]
    
    return date


# 환승 구간 / 채팅방 필터 -> 옳밣륺 채팅방으로 라우팅
@app.route('/chat/<int:friend_id>')
def chat(friend_id):
    user1 = mongo.db.users.find_one({'id': session['id']})
    user2 = mongo.db.users.find_one({'id': friend_id})

    # 존재하는 user인가 확인
    if not user2:
        print('상대방이 DB에 존재하지 않음')
        return redirect('/')

    # 내게 쓰기
    if user1 == user2:
        room = mongo.db.rooms.find_one({
            'group': False,
            'users': user1
        })
        # 내게 쓰기 방의 유무
        if not room:
            name = naming_room()
            mongo.db.rooms.insert_one({
                'name' : name,
                'group': False,
                'users': user1
            })
        else:
            name = room['name']
    # 다른 사람하고 채팅
    else:
        room1 = mongo.db.rooms.find_one({
            'group': True,
            'users': [user1, user2]
        })
        room2 = mongo.db.rooms.find_one({
            'group': True,
            'users': [user2, user1]
        })
 
        # 상대방과 과거 채팅 유무 
        if not room1 and not room2:
            name = naming_room()
            mongo.db.rooms.insert_one({
                'name' : name,
                'group': True,
                'users': [user1, user2] 
            })
        else:
            if room1:
                name = room1['name']
            else:
                name = room2['name']

    url = '/chat/room/' + name
    return redirect(url)


# 채팅 구간
@app.route('/chat/room/<room_name>')
def chatting_room(room_name):
    if not 'access_token' in session:
        print('session이 존재하지 않음')
        return redirect('/')

    me = mongo.db.users.find_one({'id': int(session['id'])})
    if not me:
        print(room_name + ' 방 - 세션과 일치하는 유저 정보가 없음')
        session.clear()
        return redirect('/')
    
    room = mongo.db.rooms.find_one({'name': room_name})
    
    return render_template('test.html', me=me, \
            room_name=room_name, room=room, date=make_date())
