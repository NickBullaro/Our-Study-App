"""
models.py
Database models for SQLAlchemy
"""
from enum import Enum
import random
import json
import flask_sqlalchemy

DB = flask_sqlalchemy.SQLAlchemy()
ROOM_PASSWORD_LENGTH = 4

class Messages(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(120))
    message = DB.Column(DB.Text, nullable=False)
    room = DB.Column(DB.String(120))
    sid = DB.Column(DB.String(120))
    picUrl = DB.Column(DB.Text)

    def __init__(self, user, message):
        self.sid = user["sid"]
        self.username = user["username"]
        self.room = user["room"]
        self.picUrl = user['picUrl']
        self.message = message

    def __repr__(self):
        return {
            "name": self.username,
            "sid": self.sid,
            "room": self.room,
            "picUrl": self.picUrl,
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

def GenerateCharacterPin(pin_length):
    pin = ''
    for i in range(pin_length):
        pin += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return pin
        
class Rooms(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    creator = DB.Column(DB.Integer, DB.ForeignKey(AuthUser.id), nullable=False)
    name = DB.Column(DB.String(50))
    password = DB.Column(DB.String(ROOM_PASSWORD_LENGTH))
    
    def __init__(self, roomCreator, roomName):
        self.creator = roomCreator
        self.name = roomName
        self.password = GenerateCharacterPin(ROOM_PASSWORD_LENGTH)
    
    def __repr__(self):
        return "{} (id: {} password: {}), created by {}".format(self.name, self.id, self.password, self.creator)

class Flashcards(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    question = DB.Column(DB.String(120))
    answer = DB.Column(DB.String(120))
    room = DB.Column(DB.Integer, DB.ForeignKey(Rooms.id), nullable=False)

    def __init__(self, question, answer, room):
        self.answer = answer
        self.question = question
        self.room = room

    def __repr__(self):
        return (self.question, self.answer, self.room)

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
   
class Whiteboards(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room = DB.Column(DB.Integer, DB.ForeignKey(Rooms.id), nullable=False)
    name = DB.Column(DB.String(32), nullable=False)
    save_num = DB.Column(DB.Integer, nullable=False)
    
    def __init__(self, room, name):
        self.room = room
        self.name = name
        self.save_num = 0

class WhiteboardConnections(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    whiteboard = DB.Column(DB.Integer, DB.ForeignKey(Whiteboards.id), nullable=False)
    sid = DB.Column(DB.String(32), nullable=False)
    leader = DB.Column(DB.Integer, nullable=False)
    
    def __init__(self, whiteboard, sid, leader):
        self.whiteboard = whiteboard
        self.sid = sid
        self.sid = sid
        self.leader = leader
