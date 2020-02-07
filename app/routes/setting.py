from flask import Flask, render_template, redirect, request
import requests
import json

from app import app
from app.tools import call_token
from app.constants import *


@app.route('/setting')
def setting():
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

    return render_template('setting.html', me=me)