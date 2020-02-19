from flask import Flask, render_template, redirect, \
    request, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.debug = False
app.config.from_object('config')
db = SQLAlchemy(app)
socketio = SocketIO(app)

from app.constants import *
from app import routes, events
from app.routes.profile import friend
from app.tools import get_me, load_star, naming_room
from app import models
db.create_all()


@app.route('/')
def index():
    me = None
    friends = list()
    friends_cnt = 0
    star = load_star()

    if 'access_token' in session:
        me = get_me(session['access_token'])

        if me != None:
            friends_info = friend()

            if friends_info == None:
                print(me['profile_nickname'] + ' 동의 안함')
                return render_template('agree.html', CLIENT_ID=CLIENT_ID, REDIRECT_URL=REDIRECT_URL)

            if friends_info:
                friends = friends_info['elements']
                friends_cnt = friends_info['total_count']

    return render_template('index.html', me=me, CLIENT_ID=CLIENT_ID,\
        REDIRECT_URL=REDIRECT_URL, friends=friends, \
        friends_cnt=friends_cnt, star=star)