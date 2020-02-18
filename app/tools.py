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


# 사용자 정보 요청
# https://developers.kakao.com/docs/restapi/user-management#사용자-정보-요청
def user_me(access_token):
    headers = make_auth_headers(access_token)
    req = requests.post(USER_ME_URL, headers=headers)

    my_info = json.loads(req.text)

    return my_info


def get_me(access_token):
    headers = make_auth_headers(access_token)
    response = requests.post(REQ_PROFILE_URL, headers=headers)

    data = json.loads(response.text)
    if 'nickName' in data:
        my_info = user_me(access_token)

        me = dict()
        me['id'] = my_info['id']
        me['connected_at'] = my_info['connected_at']
        me['profile_nickname'] = data['nickName']
        me['profile_thumbnail_image'] = data['thumbnailURL']

    return me


def load_star():
    res = requests.get('https://github.com/agurimon/KakaoTalk-web')

    soup = BeautifulSoup(res.content, 'html.parser')
    star = soup.find_all('a', class_='social-count')[1].text

    return star
