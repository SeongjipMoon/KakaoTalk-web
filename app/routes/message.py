from flask import Flask, render_template, redirect, request
import requests
import json

from app import app
from app.tools import *
from app.constants import *


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
    

@app.route('/chatting')
def chatting():
    me = get_me(session['access_token'])
    
    return render_template('chatting.html', me=me)


@app.route('/send/me', methods=["GET", "POST"])
def send_me(message):
    token = session.get('access_token')
    headers = make_auth_headers(token)
    web = 'http://katalk.junghub.kr'

    message_form = make_message_form(None, message, web, web)
    response = requests.post(SEND_MESSAGE_TO_ME_URL, \
        data=message_form, headers=headers)

    if response.status_code != '200' and response.status_code != '302':
        return 'error'
    
    return 'success'


@app.route('/send/friend', methods=["GET", "PORT"])
def send_friend():
    token = session.get('access_token')
    headers = make_auth_headers(token)
    web = 'https://naver.com'

    message = 'hello, world!'

    uuid = '_c_5y_LL88X90eLS4dfg1ezd5cn6w_fP_89F'
    message_form = make_message_form(uuid, message, web, web)

    response = requests.post(SEND_MESSAGE_TO_FRIEND_URL, \
        data=message_form, headers=headers)

    print(response.text)

    if response.status_code != '200' and response.status_code != '302':
        return 'error'
    
    return 'success'