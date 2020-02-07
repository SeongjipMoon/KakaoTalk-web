from flask import Flask, render_template, redirect, request
import requests
import json

app = Flask(__name__)
app.config.from_object('config')

from app import routes


@app.route('/')
def index():
    return render_template('index.html')