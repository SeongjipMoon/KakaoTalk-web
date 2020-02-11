from flask import Flask, render_template, redirect, \
    request, session
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

from app import routes
from app.tools import get_me 
from app.constants import *
    

@app.route('/')
def index():
    me = None
    if 'access_token' in session:
        me = get_me(session['access_token'])

    return render_template('index.html', me=me, CLIENT_ID=CLIENT_ID, REDIRECT_URL=REDIRECT_URL)


@app.route('/undefined')
def undefined():
    return redirect('/')