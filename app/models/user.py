from app import db
from datetime import datetime


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     id_katalk = db.Column(db.String(40), unique=True)
#     nickName = db.Column(db.String(40))

#     room

#     enter_time = db.Column(db.DateTime, default=datetime.now)
#     create_time = db.Column(db.DateTime, default=datetime.now)

#     rooms = db.relationship('Room')
#     # send_messages = db.relationship('Message', backref='user', lazy='dynamic')
#     # received_messages = db.relationship('Message', backref='user', lazy='dynamic')