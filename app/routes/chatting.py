from flask import render_template, url_for, redirect, abort
from datetime import datetime

from app import app, mongo
from app.tools import *
from app.constants import *
from app.routes.user import *


# 내 채팅 목록
@app.route('/chatting')
def chatting():
    me = mongo.db.users.find_one({'id': session['id']})
    
    rooms = list()

    for my_room in me['rooms']:
        my_rooms = mongo.db.rooms.find({'name': my_room['name']})

        for room in my_rooms:
            last_message = None
            
            if room['group'] == False:
                users = [me['nickname']]
            else:
                users = list()
                for user in room['users']:
                    if user['id'] != me['id']:
                        users.append(user['nickname'])

            if 'messages' in room:
                last_message = max(room['messages'], key=lambda x: x['created_at'])

            rooms.append({
                'room_name': room['name'],
                'users': users,
                'last_message': last_message 
            })

    return render_template('chatting.html', me=me, rooms=rooms)


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
            'users': [
                {'id': user1['id'], 'nickname': user1['nickname']}
            ]
        })
        # 내게 쓰기 방의 유무
        if not room:
            name = naming_room()
            mongo.db.rooms.insert_one({
                'name' : name,
                'group': False,
                'users': [
                    {'id': user1['id'], 'nickname': user1['nickname']}
                ]
            })
            room = mongo.db.rooms.find_one({'name': name})
            mongo.db.users.update_one(
                {'id': user1['id']}, 
                {'$push': {'rooms': room}}
            )
    # 다른 사람하고 채팅
    else:
        ############### 한번에 찾는거 필요함##############     
        room1 = mongo.db.rooms.find_one({
            'group': True,
            'users': [
                {'id': user1['id'], 'nickname': user1['nickname']},
                {'id': user2['id'], 'nickname': user2['nickname']}
            ]
        })

        room2 = mongo.db.rooms.find_one({
            'group': True,
            'users': [
                {'id': user2['id'], 'nickname': user2['nickname']},
                {'id': user1['id'], 'nickname': user1['nickname']}
            ]
        })
        ##############################################  

        # 상대방과 과거 채팅 유무 
        if not room1 and not room2:
            name = naming_room()
            mongo.db.rooms.insert_one({
                'name' : name,
                'group': True,
                'users': [
                    {'id': user1['id'], 'nickname': user1['nickname']},
                    {'id': user2['id'], 'nickname': user2['nickname']}
                ]
            })
            
            room = mongo.db.rooms.find_one({'name': name})
            mongo.db.users.update_one(
                {'id': user1['id']}, 
                {'$push': {'rooms': room}}
            )
            mongo.db.users.update_one(
                {'id': user2['id']}, 
                {'$push': {'rooms': room}}
            )
        else:
            if room1:
                room = room1
            else:
                room = room2

    url = '/chat/room/' + room['name']
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
