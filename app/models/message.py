from app import db
from datetime import datetime


# class Message(db.Model):
#     __tablename__ = 'messages'
#
#     id = db.Column(db.Integer, primary_key=True)
#     room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
#     sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#     content = db.Column(db.Text)
#
#     create_time = db.Column(db.DateTime, default=datetime.now)
