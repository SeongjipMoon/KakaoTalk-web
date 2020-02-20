from flask import Flask, render_template, redirect, \
    request, session
import requests
import json

from app import app
from app.tools import *
from app.constants import *


def friend(access_token):
    headers = make_auth_headers(access_token)
    url = 'https://kapi.kakao.com/v1/api/talk/friends'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200 or response.status_code == 302:
        ddict = json.loads(response.text)
        friends = list()

        for friend in ddict['elements']:
            friends.append({
                'id': int(friend['id']),
                'uuid': friend['uuid'],
                'nickname': friend['profile_nickname'],
                'thumbnail_image': friend['profile_thumbnail_image']
            })
            
        cnt = ddict['total_count']
        return True, friends, cnt
        
    return False, list(), 0