from flask import Flask, render_template, redirect, \
    request, session
import requests
import json
import os

from app import app, db
from app.tools import get_me
from app.constants import *
from app.models.room import *

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
    me = get_me(access_token)

    id_katalk = me['id']
    nickName = me['profile_nickname']

    user = User.query.filter_by(id_katalk=str(id_katalk), nickName=nickName).all()

    if not user:
        user = User(id_katalk=str(id_katalk), nickName=nickName)
        db.session.add(user)
        db.session.commit()
    
    session['id'] = str(me['id'])
    session['session'] = os.urandom(24)
    session['access_token'] = access_token
    session['profile_nickname'] = me['profile_nickname']
    session['profile_img'] = me['profile_thumbnail_image']

    return redirect('/')


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

    session.clear()

    return redirect('/')


# 앱 연결 해제
@app.route('/unlink')
def unlink():
    headers = get_auth_headers()
    response = requests.post(UNLINK_URL, headers=headers)

    user = User.query.filter_by(id_katalk=session['id'])

    if user.count() > 0:
        db.session.delete(user.first())
        db.session.commit()

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
