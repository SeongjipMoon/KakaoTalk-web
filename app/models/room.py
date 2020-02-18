from app import db
from datetime import datetime


class UserInRoom(db.Model):
    __tablename__ = 'userinrooms'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    enter_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship('User', secondary='userinrooms')
    # messages = db.relationship('Message', backref='room', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    id_katalk = db.Column(db.String(40), unique=True)
    nickName = db.Column(db.String(40))

    enter_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)

    rooms = db.relationship('Room', secondary='userinrooms')
    # send_messages = db.relationship('Message', backref='user', lazy='dynamic')
    # received_messages = db.relationship('Message', backref='user', lazy='dynamic')