from flask import Flask, render_template, redirect, \
    request, session
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

app = Flask(__name__)

app.debug = False
app.config.from_object('config')
socketio = SocketIO(app)
mongo = PyMongo(app)

from config import *
from app import routes, events
from app.routes.profile import friend
from app.tools import load_star, naming_room


@app.route('/check/<data>')
def check(data):
    if data == 'users':
        aa = mongo.db.users.find({})
    elif data == 'rooms':
        aa = mongo.db.rooms.find({})
    elif data == 'messages':
        aa = mongo.db.messages.find({})
    
    print('------------------------------')
    for a in aa:
        print(a, '\n')
    print('------------------------------')

    return redirect('/')


@app.route('/reset/<data>')
def reset(data):
    if data == 'users':
        mongo.db.users.remove()
    elif data == 'rooms':
        mongo.db.rooms.remove()
    elif data == 'messages':
        mongo.db.messages.remove()

    check(data)
    return redirect('/')


@app.route('/')
def index():
    me = None
    friends_cnt = 0
    friends = list()

    # session이 있나 없나
    if 'access_token' in session:
        # session은 있는데 디비에 없을 경우
        me = mongo.db.users.find_one({"id": session['id']})

        # 다시 재가입
        if not me:
            session.clear()
            return redirect('/')

        access_token = session['access_token']
        ok, friends, friends_cnt = friend(access_token)
        # 회원가입에서 친구목록 동의 했냐 안했냐
        if ok is False:
            print(me['nickname'] + ' 동의 안함')
            return render_template('agree.html', \
                CLIENT_ID=CLIENT_ID, \
                REDIRECT_URL=REDIRECT_URL)

    return render_template('index.html', \
        CLIENT_ID=CLIENT_ID, REDIRECT_URL=REDIRECT_URL, \
        friends=friends, friends_cnt=friends_cnt, \
        star='1.4k', me=me)