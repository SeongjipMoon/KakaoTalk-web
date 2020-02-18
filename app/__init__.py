from flask import Flask, render_template, redirect, \
    request, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
socketio = SocketIO(app)

from app.constants import *
from app import routes, events
from app.routes.profile import friend
from app.tools import get_me, load_star, naming_room
from app import models
db.create_all()

from app.models.room import *

@app.route('/')
def index():
    me = None
    friends = list()
    friends_cnt = 0
    star = load_star()

    if 'access_token' in session:
        me = get_me(session['access_token'])
        friends_info = friend()

        try:
            friends = friends_info['elements']
            friends_cnt = friends_info['total_count']
        except:
            requests.get('https://kauth.kakao.com/oauth/authorize?client_id=1714c2d9871d0b439f21d27c38051dc4&redirect_uri=http://localhost:8080/oauth&response_type=code&scope=friends')

    return render_template('index.html', me=me, CLIENT_ID=CLIENT_ID,\
        REDIRECT_URL=REDIRECT_URL, friends=friends, \
        friends_cnt=friends_cnt, star=star)