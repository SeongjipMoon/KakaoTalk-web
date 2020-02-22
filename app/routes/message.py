from flask import Flask, render_template, redirect, request, session
import requests
import json

from app import app, mongo
from app.tools import *
from app.constants import *
from app.routes.profile import *

def make_message_form(friend, message, web_url, mobile_web_url):
    payloadDict = dict({
        "object_type": "text",
        "text": "",
        "link": {
            "web_url": "",
            "mobile_web_url": ""
        }
    })

    payloadDict["text"] = message
    payloadDict["link"]["web_url"] = web_url
    payloadDict["link"]["mobile_web_url"] = mobile_web_url
    
    message_form = 'template_object=' + str(json.dumps(payloadDict))

    if friend != None:
        data = 'receiver_uuids=[\"' + friend + '\"]&' + message_form
        return data

    return message_form


@app.route('/send/me')
def send_me(message='no content'):
    token = session.get('access_token')
    headers = make_auth_headers(token)
    web = 'http://katalk.junghub.kr'

    message_form = make_message_form(None, message, web, web)
    response = requests.post(SEND_MESSAGE_TO_ME_URL, \
        data=message_form, headers=headers)

    if response.status_code != '200' and response.status_code != '302':
        return 'error'
    
    return 'success'


@app.route('/send/friend')
def send_friend(users=list(), message='no content'):
    token = session['access_token']
    headers = make_auth_headers(token)
    web = 'https://katalkjunghub.kr'

    ok, friends, friends_cnt = friend(token)

    for user in users:
        for fd in friends:
            if user['id'] == fd['id']:
                message_form = make_message_form(
                    fd['uuid'], message, web, web
                )
                response = requests.post(SEND_MESSAGE_TO_FRIEND_URL, \
                    data=message_form, headers=headers)

                if response.status_code == '200' or response.status_code == '302':
                    print(fd['nickname'], '에게 실제 메세지 전송 실패')
                    return 'error'
                
                return 'success'