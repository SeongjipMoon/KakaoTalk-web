from flask import Flask, render_template, redirect, \
    request, session
import requests
import json
import os

from app import app, mongo
from app.tools import make_auth_headers
from app.constants import *
from config import *

'''
회원가입 절차

1. 사용자는 카카오계정으로 로그인 버튼을 클릭합니다.
2. 카카오톡 앱에 연결된 카카오계정의 자격정보(Credentials)를 통해 사용자를 인식합니다.
3. 자격정보가 올바르다면 사용자(Resource Owner)로부터 접근 자원에 대한 동의/허가를 얻습니다.
4. 위 3까지 성공적으로 수행되었다면 인증 코드(Authorization Code)가 발급됩니다. 해당 인증 코드는 Redirection URI를 기반으로 Third 앱에 전달됩니다.
5. Third 앱에서는 전달받은 인증 코드를 기반으로 사용자 토큰(Access Token, Refresh Token)을 요청하고 얻게 됩니다.
'''
def get_auth_headers():
    access_token = session['access_token']
    headers = {
        'Authorization': "Bearer " + str(access_token)
    }
    return headers


# 사용자 토큰 받기
def get_user_tocken(code):
    payload = "grant_type=authorization_code&client_id=" \
        + CLIENT_ID + "&redirect_uri=" + REDIRECT_URL + \
        "/oauth" + "&code=" + str(code)

    headers = {
        'Content-type': "application/x-www-form-urlencoded;charset=utf-8",
        'Cache-Control': "no-cache"
    }

    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']

    return access_token


@app.route('/oauth')
def oauth():
    code = request.args.get('code')

    access_token = get_user_tocken(code)
    me = user_me(access_token)

    user = mongo.db.users.find_one({
        "id": me['id'], 
        "nickname": me['nickname']
    })
    
    if not user:
        mongo.db.users.insert(me)
    
    session['id'] = me['id']
    session['nickname'] = me['nickname']
    session['session'] = os.urandom(18)
    session['access_token'] = access_token
    if 'profile_image' in me:
        session['profile_image'] = me['profile_image']
    else:
        session['profile_image'] = ''

    print(me['nickname'] + ' 로그인')

    return redirect('/')


# 사용자 정보 요청
# https://developers.kakao.com/docs/restapi/user-management#사용자-정보-요청
def user_me(access_token):
    headers = make_auth_headers(access_token)
    req = requests.post(USER_ME_URL, headers=headers)

    my_info = json.loads(req.text)

    me = dict()

    me['id'] = my_info['id']
    me['nickname'] = my_info['properties']['nickname']

    if 'profile_image' in my_info['properties']:
        me['profile_image'] = my_info['properties']['profile_image']
    if 'thumbnail_image' in my_info['properties']:
        me['thumbnail_image'] = my_info['properties']['thumbnail_image']
    me['connected_at'] = my_info['connected_at']
    me['rooms'] = list()

    return me


# 갑작스러운 세션 만료를 대비한 로그인
@app.route('/login')
def login():
    return render_template('login.html', \
        CLIENT_ID=CLIENT_ID, REDIRECT_URL=REDIRECT_URL)


# 로그아웃
@app.route('/logout')
def logout():
    headers = get_auth_headers()
    response = requests.post(LOGOUT_URL, headers=headers)
    print(session['nickname'] + ' 로그아웃')
    session.clear()

    return redirect('/')


# 앱 연결 해제
@app.route('/unlink')
def unlink():
    headers = get_auth_headers()
    response = requests.post(UNLINK_URL, headers=headers)

    mongo.db.users.remove({'id': session['id']})
    mongo.db.rooms.remove({'users.id': session['id']})
    mongo.db.messages.remove({'senders.id': session['id']})
    mongo.db.messages.remove({'receviers.id': session['id']})
    print(session['nickname'] + ' 회원탈퇴')
    session.clear()

    return redirect('/')


# 사용자 리스트 요청
# https://developers.kakao.com/docs/restapi/user-management#사용자-리스트-요청
@app.route('/user/list')
def user_list():
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + ''
    }

    res = requests.get(USER_LIST_URL, headers=headers)
    print(res.text)

    return redirect('/')


# 사용자 토큰 유효성 검사 및 정보 얻기
# https://developers.kakao.com/docs/restapi/user-management#사용자-토큰-유효성-검사-및-정보-얻기
@app.route('/user/access/token/info')
def user_access_token_info():
    url = 'https://kapi.kakao.com/v1/user/access_token_info'
    headers = get_auth_headers()

    res = requests.get(url, headers=headers)
    print(res.text)

    return redirect('/')


# 동적동의
# https://developers.kakao.com/docs/restapi/user-management#동적동의
