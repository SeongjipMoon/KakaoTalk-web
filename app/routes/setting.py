from flask import Flask, render_template, redirect,\
     request, session
import requests
import json

from app import app
from app.tools import get_me
from app.constants import *


@app.route('/setting')
def setting():
    me = get_me(session['access_token'])
    
    return render_template('setting.html', me=me)