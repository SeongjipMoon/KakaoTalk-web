from flask import render_template, url_for, redirect, abort
from datetime import datetime

from app import app
from app.tools import *
from app.constants import *
from app.routes.user import *
from app.models.room import *


def make_date():
    week = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    now = datetime.now()
    date = str(now.year) + '년 ' + str(now.month) + \
        '월 ' + str(now.day) + '일 ' + \
        week[now.weekday()]
    
    return date


# 환승 구간 / 채팅방 필터 -> 옳밣륺 채팅방으로 라우팅
@app.route('/chat/<friend_id>')
def chat(friend_id):
    user1 = User.query.filter_by(id_katalk=session['id'])
    user2 = User.query.filter_by(id_katalk=friend_id)

    # 존재하는 user인가 확인
    if user1.count() <= 0 or user2.count() <= 0:
        print('상대방이 DB에 존재하지 않음')
        return redirect('/')

    user1 = user1.first()
    user2 = user2.first()

    # 내게 쓰기
    if user1 == user2:
        # 방에 사람이 혼자 있는가로 내게 쓰기 채팅방 분류
        for room in user1.rooms:
            if len(room.users) == 1:
                break
        else:
            name = naming_room()

            room = Room(name=name)
            room.users.append(user1)
            db.session.add(room)
            db.session.commit()
    # 다른 사람하고 채팅
    else:
        # 상대방과 과거 채팅 유무 
        for room in user1.rooms:
            ## sqlalchemy.orm.exc.FlushError
            if room in user2.rooms:
                break
        else:
            name = naming_room()

            room = Room(name=name)
            room.users.append(user1)
            room.users.append(user2)
            db.session.add(room)
            db.session.commit()

    url = '/chat/room/' + room.name

    return redirect(url)


# 채팅 구간
@app.route('/chat/room/<room_name>')
def chatchat(room_name):    
    date = make_date()

    # 본인 검사
    if not 'access_token' in session:
        return redirect('/')
    me = get_me(session['access_token'])

    user = User.query.filter_by(id_katalk=me['id'])
    if user.count() <= 0:
        return redirect('/login')
    user = user.first()

    # 방 주인 검사
    room = Room.query.filter_by(name=room_name)
    if room.count() <= 0:
        return redirect('/login')
    room = room.first()
    
    # 모든게 OK
    if user in room.users:
        return render_template('test.html', me=me, \
            room=room_name, users=room.users, date=date)
