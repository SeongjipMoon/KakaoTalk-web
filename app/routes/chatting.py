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
    if user1.count() <= 0 and user2.count() <= 0:
        abort(404)

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
    me = get_me(session['access_token'])
    
    date = make_date()
    
    return render_template('test.html', me=me, \
                    room=room_name, date=date)