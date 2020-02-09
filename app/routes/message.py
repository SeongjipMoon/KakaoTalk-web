from flask import Flask, render_template, redirect, request
import requests
import json

from app import app
from app.tools import call_token


@app.route('/chatting')
def chatting():
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

        access_token = call_token()

        url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
        headers = { 
            'Content-Type' : "application/x-www-form-urlencoded",
            'Cache-Control' : "no-cache",
            'Authorization': "Bearer " + str(access_token)
        }

        payloadDict = dict({
            "object_type": "text",
            "text": "test",
            "link": {
                "web_url": "https://agurimon.github.io",
                "mobile_web_url": "https://agurimon.github.io"
            }
        })

        payloadDict["text"] = message

        payload = 'template_object=' + str(json.dumps(payloadDict))

        response = requests.request("POST", url, data=payload, headers=headers)

    return redirect('/')