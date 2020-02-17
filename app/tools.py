from flask import Flask, render_template, redirect, \
    request, session
from bs4 import BeautifulSoup
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
        me = dict()
        me['profile_nickname'] = data['nickName']
        me['profile_thumbnail_image'] = data['thumbnailURL']

    return me


def load_star():
    res = requests.get('https://github.com/agurimon/KakaoTalk-web')

    soup = BeautifulSoup(res.content, 'html.parser')
    star = soup.find_all('a', class_='social-count')[1].text

    return star
