import requests
import json

from app.constants import *


def save_token(access_token):
    f = open(TOKEN_ROUTE, 'w')
    f.write(access_token)
    f.close()


def call_token():
    f = open(TOKEN_ROUTE, 'r')
    access_token = f.read()
    f.close()

    return access_token


def make_auth_headers():
    access_token = call_token()
    headers = HEADERS.copy()
    headers['Authorization'] = 'Bearer ' + str(access_token)
    return headers
    

def get_me(me=None):
    headers = make_auth_headers()
    response = requests.post(REQ_PROFILE_URL, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    
    return me