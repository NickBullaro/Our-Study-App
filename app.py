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

def db_init():
    DB.create_all()
    DB.session.commit()

socketio = flask_socketio.SocketIO(APP)
socketio.init_app(APP, cors_allowed_origins="*")

def emit_joined_rooms(user_id, client_room):
    # TODO Get this list of rooms the user has joineed already from the database
    roomList = [{"roomName": "not necessarily unique", "roomId": 0}, {"roomName": "Insert creative name here", "roomId": 2}]
    socketio.emit(
        "updated room list",
        {
            "rooms": roomList
        },
        room=client_room,
    )
    
@socketio.on("connect")
def on_connect():
    print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    print("someone disconnected!")


@socketio.on("new room creation request")
def on_new_room_creation(data):
    print("received a new room creation request: {}".format(data["roomName"]))
    #TODO
    emit_joined_rooms("temp", request.sid)


@socketio.on("join room request")
def on_join_room_request(data):
    print("received a request to join room {} with this password: {}".format(data["roomId"], data["roomPassword"]))
    #TODO
    emit_joined_rooms("temp", request.sid)


@socketio.on("new user login")
def accept_login(data):
    socketio.emit(
        "login accepted",
        {
            "email": data['email']
        },
        room=request.sid,
    )
    emit_joined_rooms("temp", request.sid)


@socketio.on("room entry request")
def accept_room_entry(data):
    socketio.emit(
        "room entry accepted",
        {
            "email": ""
        },
        room=request.sid,
    )


@socketio.on("leave room")
def accept_room_departure(data):
    socketio.emit(
        "left room",
        {
            "email": ""
        },
        room=request.sid,
    )
    emit_joined_rooms("temp", request.sid)

@APP.route("/")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    #db_init()
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
