from flask import Flask, render_template, redirect, \
    request, session
import requests
import json

from app import app
from app.tools import *
from app.constants import *


def friend():
    token = session.get('access_token')
    headers = make_auth_headers(token)
    url = 'https://kapi.kakao.com/v1/api/talk/friends'
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200 or response.status_code == 302:
        friends = json.loads(response.text)
        
        return friends
    
    return list()