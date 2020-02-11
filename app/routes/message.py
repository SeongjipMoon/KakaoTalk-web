from flask import Flask, render_template, redirect, request
import requests
import json

from app import app
from app.tools import *
from app.constants import *


def make_message_form(message, web_url, mobile_web_url):
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
    
    payload = 'template_object=' + str(json.dumps(payloadDict))

    return payload
    

@app.route('/chatting')
def chatting():
    me = get_me(session['access_token'])
    
    return render_template('chatting.html', me=me)


# @app.route('/chatting/me')
# def chatting_me():
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
    me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data
        me = None
    access_token = call_token()

    url = 'https://kapi.kakao.com/v1/api/talk/profile'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': "Bearer " + str(access_token) 
    }
    response = requests.post(url, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        me = data

    return render_template('index.html', me=me)


@app.route('/send/me', methods=["GET", "POST"])
def send_me():
    if request.method == 'POST':
        message = request.form['message']

        headers = make_auth_headers()

        web = 'https://naver.com'

        message_form = make_message_form(message, web, web)
        response = requests.request("POST", SEND_MESSAGE_ME_TO_URL, \
            data=message_form, headers=headers)

        if response.status_code == '404':
            return 'error'

    return redirect('/')