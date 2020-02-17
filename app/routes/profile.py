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

    friends = json.loads(response.text)
    
    return friends