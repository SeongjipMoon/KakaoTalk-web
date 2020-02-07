from flask import Flask, render_template, redirect, request
import requests
import json

from app import app
from app.tools import call_token
from app.constants import *


@app.route('/friend')
def friend():
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/friends'
    headers = { 
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) }
    response = requests.get(url, headers=headers)

    print(response.text)

    return redirect('/')