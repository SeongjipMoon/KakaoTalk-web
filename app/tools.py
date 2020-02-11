from flask import Flask, render_template, redirect, \
    request, session
import requests
import json

from app.constants import *


def make_auth_headers(access_token):
    headers = HEADERS.copy()
    headers['Authorization'] = 'Bearer ' + str(access_token)
    return headers
    

def get_me(access_token):
    headers = make_auth_headers(access_token)
    response = requests.post(REQ_PROFILE_URL, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    
    return me