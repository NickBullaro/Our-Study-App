"""
mock<Models.py
This is a version of models.py contains versions of the classes
defined in models.py to be used in tests. The attributes defined
ouside of the class functions will be removed and replaced with 
the same code in each class. The method will be copied and pasted
directly from the models.py versions (with 2 lines added to the
constructor for each class)

NOTES:
This assumes all the mocked classes are meant to be databases and
have an id as the primary key that is automatically assigned
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models
from models import AuthUserType
from models import GenerateCharacterPin

class Messages:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, user, message):
        self.id = type(self)._id
        type(self)._id += 1
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

class AuthUser:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, auth_type, name, email, pic=''):
        self.id = type(self)._id
        type(self)._id += 1
        assert type(auth_type) is AuthUserType
        self.auth_type = auth_type.value
        self.username = name
        self.email = email
        self.picUrl = pic
        
class Rooms:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, roomCreator, roomName):
        self.id = type(self)._id
        type(self)._id += 1
        self.creator = roomCreator
        self.name = roomName
        self.password = GenerateCharacterPin(ROOM_PASSWORD_LENGTH)
    
    def __repr__(self):
        return "{} (id: {} password: {}), created by {}".format(self.name, self.id, self.password, self.creator)

class Flashcards:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, question, answer, room):
        self.id = type(self)._id
        type(self)._id += 1
        self.answer = answer
        self.question = question
        self.room = room

    def __repr__(self):
        return (self.question, self.answer, self.room)

class CurrentConnections:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, sid, user):
        self.id = type(self)._id
        type(self)._id += 1
        self.sid = sid
        self.user = user

    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, user, room):
        self.user = user
        self.room = room

class EnteredRooms:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding two lines to __init__ for self.id)
    def __init__(self, user, room):
        self.id = type(self)._id
        type(self)._id += 1
        self.user = user
        self.room = room
