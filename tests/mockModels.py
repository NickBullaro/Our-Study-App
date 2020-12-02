"""
mock<Models.py
This is a version of models.py contains versions of the classes
defined in models.py to be used in tests. The attributes defined
ouside of the class functions will be removed and replaced with 
the same code in each class. The method will be copied and pasted
directly from the models.py versions (with 1 line added to the
constructor for each class initializing id to None). The id attribute
is meant to serve as a flag. Instances of a class that are not added
to the _db_dict property will have an id of None. Adding will set the
id to an integer value.

NOTES:
This assumes all the mocked classes are meant to be databases and
have an id as the primary key that is automatically assigned.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models
from models import AuthUserType
from models import GenerateCharacterPin
from models import ROOM_PASSWORD_LENGTH

class Messages:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, user, message):
        self.sid = user["sid"]
        self.username = user["username"]
        self.room = user["room"]
        self.picUrl = user['picUrl']
        self.message = message
        self.id = None

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
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, auth_type, name, email, pic=''): 
        assert type(auth_type) is AuthUserType
        self.auth_type = auth_type.value
        self.username = name
        self.email = email
        self.picUrl = pic
        self.id = None

class Rooms:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, roomCreator, roomName):
        self.creator = roomCreator
        self.name = roomName
        self.password = GenerateCharacterPin(ROOM_PASSWORD_LENGTH)
        self.id = None
    
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
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, question, answer, room):
        self.answer = answer
        self.question = question
        self.room = room
        self.id = None

    def __repr__(self):
        return "{} {} {}".format(self.question, self.answer, self.room)

class CurrentConnections:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self, id = None):
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, sid, user):
        self.sid = sid
        self.user = user
        self.id = None

    def __repr__(self):
        return("(id: {}, sid: {}, user_id: {})".format(self.id, self.sid, self.user))

class EnteredRooms:
    # THIS PART IS NEW FOR THE MOCKED CLASS
    _db_dict = {}
    _id = 0
    
    def get_db(self):
        return type(self)._db_dict
        
    db_dict = property(get_db)

    def add(self):
        if self.id == None:
            if id == None or not isinstance(id, int):
                self.id = type(self)._id
                type(self)._id += 1
            else:
                self.id = id
                type(self)._id = max(id + 1, type(self)._id)
            type(self)._db_dict[self.id] = self
    
    def remove(self):
        if self.id in type(self)._db_dict:
            type(self)._db_dict.pop(self.id)
            self.id = None

    @staticmethod
    def reset_mock_database():
        CurrentConnections._db_dict = {}
        CurrentConnections._id = 0

    # THIS PART IS COPIED AND PASTED FROM MODELS.PY (adding one line to __init__ for self.id)
    def __init__(self, user, room):
        self.user = user
        self.room = room
        self.id = None
