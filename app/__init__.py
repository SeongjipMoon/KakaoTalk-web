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

        # 메세지 읽음 안읽음
        receive_messages = mongo.db.messages.find({'receivers.id': session['id']})
        
        no_read = list()

        for message in receive_messages:
            for receiver in message['receivers']:
                if receiver['id'] == session['id'] and receiver['view'] == False:
                    no_read.append(message['room_name'])

    return render_template('index.html', \
        CLIENT_ID=CLIENT_ID, REDIRECT_URL=REDIRECT_URL, \
        friends=friends, friends_cnt=friends_cnt, \
        star='1.4k', me=me, no_read=len(no_read))