"""
app.py
Main module for the app
"""
import os
from dotenv import load_dotenv
import flask
import flask_socketio
import models


APP = flask.Flask(__name__)
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "keys.env")
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
testUsers = ["Nick", "Jason", "Mitchell", "George", "Navado"]

NEW_CARDS = "new cards"
CARDS = "cards"

SAMPLE_MESSAGES = []


def emit_joined_rooms(client_room):
    '''
    Takes in a clients personal room sid and uses it to identify the user in the database. It then checks
    the database to see which rooms the user has joined and emits that as a list to rhe client_room
    '''
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=client_room).first()
    room_id_list = models.DB.session.query(models.JoinedRooms.room).filter_by(user=user_id).all()
    models.DB.session.commit()
    room_list = []
    for room_id in room_id_list:
        room_list.append({
            'roomName': models.DB.session.query(models.Rooms.name).filter_by(id=room_id).first(),
            'roomId': room_id
        })
    socketio.emit(
        "updated room list",
        {"rooms": room_list},
        room=client_room,
    )

def get_room(client_sid):
    '''
    Takes in the a client's personal room sid and returns the room id of the room the client is 
    currently in. If the client is not currently in any rooms, this just returns the client's \
    personal sid
    '''
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=client_sid).first()
    entered_room = models.DB.session.query(models.EnteredRooms.room).filter_by(user=user_id).first()
    if entered_room:
        return str(entered_room[0])
    else:
        return client_sid
    

def emit_flashcards(room):
    """Emit all the flashcards for a specific room"""
    all_cards = models.Flashcards.query.all()
    cards = []
    for card in all_cards:
        card_dict = {}
        card_dict["question"] = card.question
        card_dict["answer"] = card.answer
        cards.append(card_dict)

    socketio.emit(CARDS, cards, room=room)

def emit_all_messages(room_id):
    # TODO properly load the messages realted to the room from the database
    all_messages = models.DB.session.query(models.Messages.message).filter_by(room=room_id).all()
    print("messages: ", all_messages)
    socketio.emit(
        "sending message history", {"allMessages": all_messages}, room=room_id
    )


def emit_room_history(room_id):

    emit_flashcards(room_id)
    # TODO properly load the messages realted to the room from the database
    message_history = SAMPLE_MESSAGES
    data = {"allMessages": message_history}
    socketio.emit("sending room data", data, room=room_id)


def emit_all_users(channel, roomID):
    all_user_ids = models.DB.session.query(models.EnteredRooms.user).filter_by(room=roomID).all()
    all_users = []
    for i in all_user_ids:
        all_users.append(models.DB.session.query(models.AuthUser.username).filter_by(id=i).first()[0])
    print("users: ", all_users)
    socketio.emit(channel, {"all_users": all_users})

def clear_non_persistent_tables():
    '''
    EnteredRooms and CurrentConnections are tables the server uses to track the current state of rooms. Both
    tables should be empty on startup.
    '''
    models.DB.session.query(models.CurrentConnections).delete()
    models.DB.session.query(models.EnteredRooms).delete()
    models.DB.session.commit()


@socketio.on("connect")
def on_connect():
    print("Someone connected!")
    models.DB.session.add(models.CurrentConnections(flask.request.sid, None))
    models.DB.session.commit()


@socketio.on("disconnect")
def on_disconnect():
    '''
    When a user disconnects, make sure they are removed from any rooms that they had entered and 
    stop associating the user with that connection
    '''
    disconnected_user = models.DB.session.query(models.CurrentConnections).filter_by(sid=flask.request.sid).first()
    if not disconnected_user:
        print("Database error on disconnect")
        return
    elif disconnected_user.user is not None:
        # Remove the user from any rooms they are currently in
        user_room = get_room(flask.request.sid)
        models.DB.session.query(models.EnteredRooms).filter_by(user=disconnected_user.user).delete()
        models.DB.session.commit()
        # Update the room members for anyone still in the room
        emit_all_users(USERS_RECEIVED_CHANNEL, user_room)
        # get the disconnected user's username
        disconnected_username = models.DB.session.query(models.AuthUser).filter_by(id=disconnected_user.user).first().username
    else:
        disconnected_username = 'unlogged-in user'
    print("{} disconnected!".format(disconnected_username))
    # Stop tracking that connection between user and sid
    models.DB.session.delete(disconnected_user)
    models.DB.session.commit()


@socketio.on("new room creation request")
def on_new_room_creation(data):
    print("received a new room creation request: {}".format(data["roomName"]))
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=flask.request.sid).first()
    new_room = models.Rooms(user_id, data['roomName'])
    models.DB.session.add(new_room)
    models.DB.session.commit()
    models.DB.session.refresh(new_room)
    models.DB.session.add(models.JoinedRooms(user_id, new_room.id))
    models.DB.session.commit()
    print("created new room:\n\t{}".format(new_room))
    emit_joined_rooms(flask.request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, new_room.id)
    emit_all_messages(new_room.id)


@socketio.on("join room request")
def on_join_room_request(data):
    print(
        "received a request to join room {} with this password: {}".format(
            data["roomId"], data["roomPassword"]
        )
    )
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=flask.request.sid).first()
    room = models.DB.session.query(models.Rooms).filter_by(id=data['roomId'], password=data['roomPassword']).first()
    if room:
        models.DB.session.add(models.JoinedRooms(user_id, room.id))
    emit_joined_rooms(flask.request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, room.id)
    emit_all_messages(room.id)


@socketio.on("new google user login")
def accept_google_login(data):
    socketio.emit(
        "login accepted",
        room=flask.request.sid
    )
    user = models.DB.session.query(models.AuthUser).filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data['email']).first()
    if not user:
        print('adding new user')
        models.DB.session.add(models.AuthUser(models.AuthUserType.GOOGLE, data['user'], data['email'], data['pic']))
        models.DB.session.commit()
        user = models.DB.session.query(models.AuthUser).filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data['email']).first()
    else:
        print('updating existing user')
        user.username = data['user']
        user.picUrl = data['pic']
    connection = models.DB.session.query(models.CurrentConnections).filter_by(sid=flask.request.sid).first()
    connection.user = user.id
    models.DB.session.commit()
    print("{} logged in".format(user.username))
    emit_joined_rooms(flask.request.sid)


@socketio.on("room entry request")
def on_room_entry_request(data):
    print(data)
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=flask.request.sid).first()
    models.DB.session.add(models.EnteredRooms(user_id, data['roomId']))
    models.DB.session.commit()
    socketio.emit("room entry accepted", room=flask.request.sid)
    flask_socketio.join_room(str(data['roomId']))
    print("room entry accepted")
    emit_room_history(flask.request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, data['roomId'])
    emit_all_messages(get_room(flask.request.sid))


@socketio.on("leave room")
def accept_room_departure(data):
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=flask.request.sid).first()[0]
    room_id = models.DB.session.query(models.EnteredRooms.room).filter_by(user=user_id).first()[0]
    models.DB.session.query(models.EnteredRooms).filter_by(user=user_id).delete()
    models.DB.session.commit()
    socketio.emit(
        "left room",
        room=flask.request.sid,
    )
    flask_socketio.leave_room(str(room_id))
    print("user {} left room {}".format(user_id, room_id))
    emit_joined_rooms(flask.request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, room_id)


@socketio.on("new message input")
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    user = {}
    user["sid"] = flask.request.sid
    user["room"] = get_room(flask.request.sid)  # TODO: get room_id from the sender request.sid
    user_id = models.DB.session.query(models.CurrentConnections.user).filter_by(sid=flask.request.sid).first()[0]
    user["username"] = models.DB.session.query(models.AuthUser.username).filter_by(id=user_id).first()[0] 
    models.DB.session.add(models.Messages(user, user['username'] + ": " + data['message']))
    models.DB.session.commit()
    emit_all_messages(get_room(flask.request.sid))


@socketio.on(NEW_CARDS)
def new_cards(data):
    """Listen for new cards event from client.
    Update the database by replacing the old cards with the new cards.
    """

    print("New cards:", data)
    room = get_room(flask.request.sid)

    models.DB.session.query(models.Flashcards).delete()
    models.DB.session.commit()

    for card in data:
        question = card["question"]
        answer = card["answer"]

        models.DB.session.add(models.Flashcards(question, answer, room))

    models.DB.session.commit()
    emit_flashcards(room)


@socketio.on("drawing stroke input")
def on_drawing_stroke(data):
    room_id = get_room(flask.request.sid)
    socketio.emit("drawing stroke output", data, room=room_id)


@APP.route("/")
def index():
    """ Return the index.html page on this route"""
    return flask.render_template("index.html")


if __name__ == "__main__":
    database_init()
    clear_non_persistent_tables()
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
