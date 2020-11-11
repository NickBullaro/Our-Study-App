'''
app.py
Main module for the app
'''

import os
import flask
import flask_socketio
import flask_sqlalchemy
import models
from dotenv import load_dotenv
from flask import request

APP = flask.Flask(__name__)
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = os.path.join(os.path.dirname(__file__), 'keys.env')
load_dotenv(DOTENV_PATH)

try:
    DATABASE_URI = os.environ["DATABASE_URL"]
except KeyError:
    DATABASE_URI = ""

APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.DB.init_app(APP)
models.DB.app = APP

def database_init():
    models.DB.create_all()
    models.DB.session.commit()

socketio = flask_socketio.SocketIO(APP)
socketio.init_app(APP, cors_allowed_origins="*")

username_sid_dict = {}

USERS_RECEIVED_CHANNEL = "users received"
users = ["Nick", "Jason", "Mitchell", "George", "Navado"]

NEW_CARDS = 'new cards'
CARDS = 'cards'

SAMPLE_JOINED_ROOMS_LIST = [
    {
        "roomName": "not necessarily unique",
        "roomId": 0
        
    },
    {
        "roomName": "Insert creative name here",
        "roomId": 2
    }]

SAMPLE_MESSAGES = []

def emit_joined_rooms(client_room):
    # TODO Get this list of rooms the user has joineed already from the database
    roomList = SAMPLE_JOINED_ROOMS_LIST
    socketio.emit(
        "updated room list",
        {
            "rooms": roomList
        },
        room=client_room,
    )

def get_room(client_sid):
    return client_sid
    
def emit_flashcards(room):
    '''Emit all the flashcards for a specific room'''
    all_cards = models.Flashcards.query.all()
    cards = []
    for card in all_cards:
        card_dict = {}
        card_dict['question'] = card.question
        card_dict['answer'] = card.answer
        cards.append(card_dict)
        
    socketio.emit(CARDS, cards)
    
def emit_all_messages(room_id):
    # TODO properly load the messages realted to the room from the database
    all_messages = SAMPLE_MESSAGES
    socketio.emit("sending message history", {"allMessages": all_messages}, room=room_id)
    
def emit_room_history(room_id):

    emit_flashcards(room_id)
    # TODO properly load the messages realted to the room from the database
    message_history = SAMPLE_MESSAGES
    data = {
        'allMessages': message_history
    }
    socketio.emit('sending room data', data, room=room_id)

def emit_all_users(channel):
    all_users = users
    socketio.emit(channel, {"all_users": all_users})
      

@socketio.on("connect")
def on_connect():
    print("Someone connected!")
    models.DB.session.add(models.CurrentConnections(request.sid, None))
    models.DB.session.commit()


@socketio.on("disconnect")
def on_disconnect():
    disconnected_user = models.CurrentConnections.query.filter_by(sid=request.sid).first()
    if not disconnected_user:
        print("Database error on disconnect")
    elif disconnected_user.user is not None:
        disconnected_username = models.AuthUser.query.filter_by(id=disconnected_user.user).first().username
    else:
        disconnected_username = 'unlogged-in user'
    print("{} disconnected!".format(disconnected_username))
    models.DB.session.delete(disconnected_user)


@socketio.on("new room creation request")
def on_new_room_creation(data):
    print("received a new room creation request: {}".format(data["roomName"]))
    #TODO Add new room to the databse and set the sender 
    emit_joined_rooms(request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL)


@socketio.on("join room request")
def on_join_room_request(data):
    print("received a request to join room {} with this password: {}".format(data["roomId"], data["roomPassword"]))
    #TODO Check the database to verify that the roomId and roomPassword are a valid pair
    #TODO If the pair is valid, update the database to reflect that the user associated with request has joineed the room
    emit_joined_rooms(request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL)


@socketio.on("new google user login")
def accept_google_login(data):
    socketio.emit(
        "login accepted",
        room=request.sid
    )
    user = models.DB.session.query(models.AuthUser).filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data['email']).first()
    if not user:
        models.DB.session.add(models.AuthUser(models.AuthUserType.GOOGLE, data['user'], data['email'], data['pic']))
        user = models.DB.session.query(models.AuthUser.id).filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data['email']).first()
    else:
        user.username = data['user']
        user.picUrl = data['pic']
    connection = models.DB.session.query(models.CurrentConnections).filter_by(sid=request.sid).first()
    connection.user = user.id
    models.DB.session.commit()
    print("{} logged in".format(user.username))
    emit_joined_rooms(request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL)


@socketio.on("room entry request")
def on_room_entry_request(data):
    socketio.emit(
        "room entry accepted",
        room=request.sid
    )
    print("room entry accepted")
    emit_room_history(request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL)


@socketio.on("leave room")
def accept_room_departure(data):
    socketio.emit(
        "left room",
        room=request.sid,
    )
    emit_joined_rooms(request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL)

@socketio.on("new message input")
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    SAMPLE_MESSAGES.append(data['message'])
    room_id = request.sid # TODO: get room_id from the sender request.sid
    emit_all_messages(room_id)
    emit_all_users(USERS_RECEIVED_CHANNEL)
    
@socketio.on(NEW_CARDS)
def new_cards(data):
    ''' Listen for new cards event from client. 
    Update the database by replacing the old cards with the new cards.
    '''
    
    print("New cards:", data)
    room = get_room(request.sid)
    
    #Clear database
    models.DB.session.query(models.Flashcards).delete()
    models.DB.session.commit()

    
    for card in data:
            question = card["question"]
            answer = card["answer"]
        
            models.DB.session.add(models.Flashcards(question, answer))
            
    models.DB.session.commit()
    emit_flashcards(room)
    emit_all_users(USERS_RECEIVED_CHANNEL)

@socketio.on("drawing stroke input")
def on_drawing_stroke(data):
    room_id = request.sid
    socketio.emit("drawing stroke output",data)
    

@APP.route("/")
def index():
    ''' Return the index.html page on this route'''
    return flask.render_template("index.html")

if __name__ == "__main__":
    database_init()
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
