from flask import render_template, url_for, redirect
from datetime import datetime

from app import app
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


# 환승 구간
@app.route('/chat/<friend_id>')
def chat(friend_id):
    my_id = session['id']

    if str(my_id) == friend_id:
        # 내게 쓰기
        room = 'jungyoon'
    else:
        room = 'apple'
        # db에서 아이디 넣고 찾는데
        # 있으면 그거 쓰고 없으면 새로 방 만듬

    url = '/chat/room/' + room

    return redirect(url)


@app.route('/chat/room/<room_name>')
def chatchat(room_name):
    me = get_me(session['access_token'])
    
    date = make_date()
    
    return render_template('test.html', me=me, \
                    room=room_name, date=date)