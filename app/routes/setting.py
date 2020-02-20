from flask import Flask, render_template, redirect,\
     request, session
import requests
import json

from app import app, mongo
from app.constants import *


@app.route('/setting')
def setting():
     me = mongo.db.users.find_one({"id": session['id']})
     return render_template('setting.html', me=me)