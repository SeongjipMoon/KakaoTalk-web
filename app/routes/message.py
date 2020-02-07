from flask import Flask, render_template, redirect, request
import requests
import json

from app import app


@app.route('/send/me')
def send_me():
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

    payload = 'template_object=' + str(json.dumps(payloadDict))
    print(payload)

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    return redirect('/')
