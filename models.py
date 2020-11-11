'''
models.py
Database models for SQLAlchemy
'''

import flask_sqlalchemy
import json
from enum import Enum

DB = flask_sqlalchemy.SQLAlchemy()

class Messages(DB.Model):
    id = DB.Column(DB.Integer,  primary_key=True)
    username = DB.Column(DB.String(120))
    message= DB.Column(DB.Text, nullable=False)
    room = DB.Column(DB.String(120))
    sid = DB.Column(DB.String(120))
    picUrl = DB.Column(DB.Text)
    
    def __init__(self, user, message):
        self.sid = user['sid']
        self.username = user['username']
        self.room = user['room']
        self.message = message
        self.picUrl = user['profilePic']
    
    def __repr__(self):
        return {'name': self.username, 'sid' : self.sid, 'room' : self.room, 'message' : self.message}

class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    username = DB.Column(DB.String(120))
    room = DB.Column(DB.String(120))
    sid = DB.Column(DB.String(120))
    password = DB.Column(DB.String(120))
    picUrl = DB.Column(DB.Text)
    
    def __init__(self, name, auth_type, password, sid, pic=''):
        assert type(auth_type) is AuthUserType
        self.username = name
        self.auth_type = auth_type.value
        self.password = password
        self.room = ''
        self.sid = sid
        self.picUrl = pic
        
class AuthUserType(Enum):
    GOOGLE = 'google'
    FACEBOOK = 'facebook'
    
class Flashcards(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    question = DB.Column(DB.String(120))
    answer = DB.Column(DB.String(120))
    #room = DB.Column(DB.String(120), DB.ForeignKey('rooms.room'), nullable=False)

    def __init__(self, question, answer):
        self.answer = answer
        self.question = question
        
    def __repr__(self):
        return '<card> question: {} answer: {} </card>\n'.format(self.question, self.answer)
