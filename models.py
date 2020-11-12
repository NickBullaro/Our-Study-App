"""
models.py
Database models for SQLAlchemy
"""
from enum import Enum
import random
import json
import flask_sqlalchemy

DB = flask_sqlalchemy.SQLAlchemy()


class Messages(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(120))
    message = DB.Column(DB.Text, nullable=False)
    room = DB.Column(DB.String(120))
    sid = DB.Column(DB.String(120))
    pic_url = DB.Column(DB.Text)

    def __init__(self, user, message):
        self.sid = user["sid"]
        self.username = user["username"]
        self.room = user["room"]
        self.message = message
        self.pic_url = user["profilePic"]

    def __repr__(self):
        return {
            "name": self.username,
            "sid": self.sid,
            "room": self.room,
            "message": self.message,
        }


class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    username = DB.Column(DB.String(120))
    email = DB.Column(DB.String(120))
    picUrl = DB.Column(DB.Text)
    
    def __init__(self, auth_type, name, email, pic=''):
        assert type(auth_type) is AuthUserType
        self.auth_type = auth_type.value
        self.username = name
        self.email = email
        self.picUrl = pic
class AuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"


class Flashcards(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    question = DB.Column(DB.String(120))
    answer = DB.Column(DB.String(120))
    # room = DB.Column(DB.String(120), DB.ForeignKey('rooms.room'), nullable=False)

    def __init__(self, question, answer):
        self.answer = answer
        self.question = question

    def __repr__(self):
        return "<card> question: {} answer: {} </card>\n".format(
            self.question, self.answer
        )

def GenerateCharacterPin(pin_length):
    pin = ''
    for i in range(pin_length):
        pin += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return pin
        
class Rooms(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    creator = DB.Column(DB.Integer, DB.ForeignKey(AuthUser.id), nullable=False)
    name = DB.Column(DB.String(50))
    password = DB.Column(DB.String(4))
    
    def __init__(self, roomCreator, roomName):
        self.creator = roomCreator
        self.name = roomName
        self.password = GenerateCharacterPin(4)
    
    def __repr__(self):
        return "{} (id: {} password: {}), created by {}".format(self.name, self.id, self.password, self.creator)

class CurrentConnections(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    sid = DB.Column(DB.String(32), nullable=False)
    user = DB.Column(DB.Integer, DB.ForeignKey(AuthUser.id), nullable=True)

    def __init__(self, sid, user):
        self.sid = sid
        self.user = user

class JoinedRooms(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.Column(DB.Integer, DB.ForeignKey(AuthUser.id), nullable=False)
    room = DB.Column(DB.Integer, DB.ForeignKey(Rooms.id), nullable=False)
    
    def __init__(self, user, room):
        self.user = user
        self.room = room

class EnteredRooms(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.Column(DB.Integer, DB.ForeignKey(AuthUser.id), nullable=False)
    room = DB.Column(DB.Integer, DB.ForeignKey(Rooms.id), nullable=False)
    
    def __init__(self, user, room):
        self.user = user
        self.room = room
