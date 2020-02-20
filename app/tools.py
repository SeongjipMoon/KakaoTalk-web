from flask import Flask, render_template, redirect, \
    request, session
from bs4 import BeautifulSoup
import requests
import json
from random import randint

from app import mongo
from app.constants import *


def make_auth_headers(access_token):
    headers = HEADERS.copy()
    headers['Authorization'] = 'Bearer ' + str(access_token)
    return headers


def load_star():
    res = requests.get('https://github.com/agurimon/KakaoTalk-web')

    soup = BeautifulSoup(res.content, 'html.parser')
    star = soup.find_all('a', class_='social-count')[1].text

    return star


def naming_room():
    num = randint(1, 522)
    cnt = 0

    f = open("animal_list.txt", "r")

    for line in f.readlines():
        cnt += 1
        if cnt == num:
            name = line.replace('\n', '').lower()

            while True:
                room = mongo.db.rooms.find_one({'name': name})

                if not room:
                    f.close()
                    return name