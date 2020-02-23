from flask import Flask, render_template, redirect, request, session
import requests
import json

from app import app, mongo
from app.tools import *
from app.constants import *
from app.routes.profile import *

def make_message_form(friend, message, room):
    payloadDict = dict({
        "object_type": "text",
        "text": "",
        "link": {
            "web_url": "",
            "mobile_web_url": ""
        },
        "button_title": "답장하러 가기"
    })

    # https://developers.kakao.com/apps -> 내 애플리케이션 
    # -> 앱 정보 -> 설정된 플랫폼 -> 사이트 도메인에 추가
    web = 'http://katalk.junghub.kr/' + room
    payloadDict["link"]["web_url"] = web
    payloadDict["link"]["mobile_web_url"] = web
    payloadDict["text"] = message

    message_form = 'template_object=' + str(json.dumps(payloadDict))

    if friend != None:
        data = 'receiver_uuids=[\"' + friend + '\"]&' + message_form
        return data

    return message_form


@app.route('/file')
def file():

    return render_template('file.html')


# 나에게 보내기
# https://developers.kakao.com/docs/restapi/kakaotalk-api#나에게-보내기
def send_me(message, room_name):
    token = session['access_token']
    headers = make_auth_headers(token)

    message_form = make_message_form(None, message, room_name)
    response = requests.post(SEND_MESSAGE_TO_ME_URL, \
        data=message_form, headers=headers)

    if response.status_code != '200' and response.status_code != '302':
        return 'error'
    
    return 'success'


# 메시지 전송
# https://developers.kakao.com/docs/restapi/kakaotalk-api#메시지-전송
def send_friend(users, message, room_name):
    token = session['access_token']
    headers = make_auth_headers(token)

    ok, friends, friends_cnt = friend(token)

    for user in users:
        for fd in friends:
            if user['id'] == fd['id']:
                message_form = make_message_form(
                    fd['uuid'], message, room_name
                )
                response = requests.post(SEND_MESSAGE_TO_FRIEND_URL, \
                    data=message_form, headers=headers)

                if response.status_code == '200' or response.status_code == '302':
                    print(fd['nickname'], '에게 실제 메세지 전송 실패')
                    return 'error'
                
                return 'success'