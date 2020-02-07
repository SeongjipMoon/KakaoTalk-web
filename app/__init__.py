from flask import Flask, render_template, redirect, request
import requests
import json

app = Flask(__name__)
app.config.from_object('config')

from app import routes
from app.tools import call_token
from app.constants import *


@app.route('/')
def index():
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data

    return render_template('index.html', me=me)
