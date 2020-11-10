import os
import flask
import flask_socketio
import flask_sqlalchemy
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

DB = flask_sqlalchemy.SQLAlchemy(APP)
DB.app = APP

import models

def db_init():
    DB.create_all()
    DB.session.commit()

socketio = flask_socketio.SocketIO(APP)
socketio.init_app(APP, cors_allowed_origins="*")

username_sid_dict = {}

NEW_CARDS = 'new card'
CARDS = 'cards'

SAMPLE_FLASH_CARDS = [
      {
        'id': 1,
        'question': 'Question 1 ',
        'answer': 'Answer 1',
      },
      {
        'id': 2,
        'question': 'Question 2 ',
        'answer': 'Answer 2',
      }]

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
    all_cards = models.Flashcards.query.all()
    cards = []
    for card in all_cards:
        card_dict = {}
        card_dict['question'] = card.question
        card_dict['answer'] = card.answer
        cards.append(card_dict)
        
    socketio.emit(CARDS, cards, room=room)
    
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
      

@socketio.on("connect")
def on_connect():
    print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    disconnected_user = username_sid_dict.pop(request.sid, 'unlogged-in user')
    print("{} disconnected!".format(disconnected_user))


@socketio.on("new room creation request")
def on_new_room_creation(data):
    print("received a new room creation request: {}".format(data["roomName"]))
    #TODO Add new room to the databse and set the sender 
    emit_joined_rooms(request.sid)


@socketio.on("join room request")
def on_join_room_request(data):
    print("received a request to join room {} with this password: {}".format(data["roomId"], data["roomPassword"]))
    #TODO Check the database to verify that the roomId and roomPassword are a valid pair
    #TODO If the pair is valid, update the database to reflect that the user associated with request has joineed the room
    emit_joined_rooms(request.sid)


@socketio.on("new user login")
def accept_login(data):
    username_sid_dict[request.sid] = data['email']
    socketio.emit(
        "login accepted",
        room=request.sid
    )
    print("{} logged in".format(data['email']))
    emit_joined_rooms(request.sid)


@socketio.on("room entry request")
def accept_room_entry(data):
    socketio.emit(
        "room entry accepted",
        room=request.sid
    )
    print("room entry accepted")
    emit_room_history(request.sid)


@socketio.on("leave room")
def accept_room_departure(data):
    socketio.emit(
        "left room",
        room=request.sid,
    )
    emit_joined_rooms(request.sid)

@socketio.on("new message input")
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    SAMPLE_MESSAGES.append(data['message'])
    room_id = request.sid # TODO: get room_id from the sender request.sid
    emit_all_messages(room_id)
    
@socketio.on(NEW_CARDS)
def new_cards(data):
    print(data)
    room = get_room(request.sid)
    DB.session.add(models.Flashcards(data['question'], data['answer']))
    DB.session.commit()
    emit_flashcards(room)

@socketio.on("drawing stroke input")
def on_drawing_stroke(data):
    room_id = request.sid
    socketio.emit("drawing stroke output",data)

@APP.route("/")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    db_init()
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
