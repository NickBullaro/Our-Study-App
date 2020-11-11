"""
models.py
Database models for SQLAlchemy
"""
from enum import Enum
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
    room = DB.Column(DB.String(120))
    sid = DB.Column(DB.String(120))
    password = DB.Column(DB.String(120))
    pic_url = DB.Column(DB.Text)

    def __init__(self, name, auth_type, password, sid, pic=""):
        assert isinstance(auth_type, AuthUserType)
        self.username = name
        self.auth_type = auth_type.value
        self.password = password
        self.room = ""
        self.sid = sid
        self.pic_url = pic


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
