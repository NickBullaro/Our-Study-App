"""
app.py
Main module for the app
"""
import os
import io
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import flask
import flask_socketio
import boto3
import models
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "keys.env")
load_dotenv(DOTENV_PATH)

roomTokens = {}

USERS_RECEIVED_CHANNEL = "users received"
NEW_CARDS = "new cards"
CARDS = "cards"

try:
    DATABASE_URI = os.environ["DATABASE_URL"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    twilio_api_key_sid = os.environ["TWILIO_API_KEY_SID"]
    twilio_api_key_secret = os.environ["TWILIO_API_KEY_SECRET"]
except KeyError:
    DATABASE_URI = ""
    AWS_ACCESS_KEY = ""
    AWS_SECRET_KEY = ""
    twilio_account_sid = ""
    twilio_api_key_sid = ""
    twilio_api_key_secret = ""

APP = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(APP)
socketio.init_app(APP, cors_allowed_origins="*")
APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

models.DB.init_app(APP)
models.DB.app = APP

def database_init():
    models.DB.create_all()
    models.DB.session.commit()

def emit_joined_rooms(client_sid):
    """
    Takes in a clients personal room sid and uses it to identify the user in the database.
    It then checks the database to see which rooms the user has joined and
    emits that as a list to the client_room
    """
    curr_conn_row = (
        models.DB.session.query(models.CurrentConnections)
        .filter_by(sid=client_sid)
        .first()
    )
    if curr_conn_row:
        user_id = curr_conn_row.user
    else:
        return
    room_id_list = (
        models.DB.session.query(models.JoinedRooms.room).filter_by(user=user_id).all()
    )
    models.DB.session.commit()
    room_list = []
    for room_id in room_id_list:
        print("HERE", room_id)
        room_list.append(
            {
                "roomName": models.DB.session.query(models.Rooms.name)
                .filter_by(id=room_id)
                .first(),
                "roomId": room_id[0],
            }
        )
    socketio.emit(
        "updated room list",
        {"rooms": room_list},
        room=str(client_sid),
    )

def get_room(client_sid):
    """
    Takes in the a client's personal room sid and returns the room id of the room the client is
    currently in. If the client is not currently in any rooms, this just returns the client's
    personal sid

    NOTE: This will always output a string. This matches with the socketio emits, but does not work
    with any database filters. Make sure to convert back to an int for database queries.
    """
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=client_sid)
        .first()
    )
    entered_room = (
        models.DB.session.query(models.EnteredRooms.room)
        .filter_by(user=user_id)
        .first()
    )
    if entered_room:
        return str(entered_room[0])
    return client_sid

def get_board(client_sid):
    """
    Takes in the a client's personal room sid
    and returns the whiteboard id of the room the client is
    currently in. If the client is not currently in any rooms, this just returns the client's
    personal sid

    NOTE: This will always output a string. This matches with the socketio emits, but does not work
    with any database filters.
    Make sure to convert back to remove w and cast to int for database queries.
    """
    board_room = (
        models.DB.session.query(models.WhiteboardConnections)
        .filter_by(sid=client_sid)
        .first()
    )
    if board_room:
        return "w{}".format(board_room.whiteboard)
    return client_sid

def emit_flashcards(room):
    """Emit all the flashcards for a specific room"""
    all_cards = models.DB.session.query(models.Flashcards).all()
    cards = []
    for card in all_cards:
        card_dict = {}
        card_dict["question"] = card.question
        card_dict["answer"] = card.answer
        cards.append(card_dict)

    socketio.emit(CARDS, cards, room=str(room))

def emit_all_messages(client_sid):
    room_id = get_room(client_sid)
    # If the user isn't in a room, emit nothing
    if room_id == client_sid:
        return
    all_messages = (
        models.DB.session.query(models.Messages.message).filter_by(room=room_id).all()
    )
    all_user_pics = (
        models.DB.session.query(models.Messages.picUrl).filter_by(room=room_id).all()
    )
    print("--", all_user_pics)

    socketio.emit(
        "sending message history",
        {"allMessages": all_messages, 'all_user_pics': all_user_pics},
        room=str(room_id)
    )

def emit_room_history(client_sid):
    room_id = get_room(client_sid)
    emit_flashcards(client_sid)
    emit_all_messages(client_sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, client_sid)
    emit_room_stats(client_sid)

def emit_all_users(channel, client_sid):
    room_id = get_room((client_sid))
    # If the user isn't in a room, emit nothing
    if room_id == client_sid:
        return
    entered_room_rows = models.DB.session.query(models.EnteredRooms).filter_by(room=room_id).all()
    all_user_ids = []
    all_users = []
    all_user_pics = []
    for entered_room_row in entered_room_rows:
        user_row = (
            models.DB.session.query(models.AuthUser).filter_by(id=entered_room_row.user).first()
        )
        if user_row:
            all_users.append(user_row.username)
            all_user_pics.append(user_row.picUrl)
            all_user_ids.append(user_row.id)
    print("users: ", all_users)
    socketio.emit(channel, {"all_users": all_users, 'all_user_pics': all_user_pics, 'all_user_ids': all_user_ids}, room=str(room_id))

def emit_room_stats(client_sid):
    room_id = get_room(client_sid)
    # If the user isn't in a room, emit nothing
    if room_id == client_sid:
        return
    room_row = models.DB.session.query(models.Rooms).filter_by(id=int(room_id)).first()
    if room_row:
        socketio.emit("room stats update", {'roomId':room_row.id, 'roomPassword': room_row.password, 'roomName': room_row.name}, room=str(room_id))

def clear_non_persistent_tables():
    """
    EnteredRooms and CurrentConnections are tables the server
    uses to track the current state of rooms.
    Both tables should be empty on startup.
    """
    models.DB.session.query(models.CurrentConnections).delete()
    models.DB.session.query(models.EnteredRooms).delete()
    models.DB.session.query(models.WhiteboardConnections).delete()
    models.DB.session.commit()

@socketio.on("connect")
def on_connect():
    print("Someone connected!")
    models.DB.session.add(models.CurrentConnections(flask.request.sid, None))
    models.DB.session.commit()

@socketio.on("disconnect")
def on_disconnect():
    """
    When a user disconnects, make sure they are removed from any rooms that they had entered and
    stop associating the user with that connection
    """
    disconnect_whiteboard(flask.request.sid)
    disconnected_user = (
        models.DB.session.query(models.CurrentConnections)
        .filter_by(sid=flask.request.sid)
        .first()
    )
    if not disconnected_user:
        print("Database error on disconnect")
        return
    elif disconnected_user.user is not None:
        # Remove the user from any rooms they are currently in
        user_room = get_room(flask.request.sid)
        models.DB.session.query(models.EnteredRooms).filter_by(
            user=disconnected_user.user
        ).delete()
        models.DB.session.commit()
        # Update the room members for anyone still in the room
        emit_all_users(USERS_RECEIVED_CHANNEL, flask.request.sid)
        # get the disconnected user's username
        disconnected_username = (
            models.DB.session.query(models.AuthUser)
            .filter_by(id=disconnected_user.user)
            .first()
            .username
        )
    else:
        disconnected_username = "unlogged-in user"
    print("{} disconnected!".format(disconnected_username))
    # Stop tracking that connection between user and sid
    models.DB.session.delete(disconnected_user)
    models.DB.session.commit()

@socketio.on("resend room selection data")
def refresh_room_selection_screen():
    emit_joined_rooms(flask.request.sid)

@socketio.on("resend in room data")
def refresh_in_room_screen():
    emit_room_history(flask.request.sid)

@socketio.on("new room creation request")
def on_new_room_creation(data):
    print("received a new room creation request: {}".format(data["roomName"]))
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()
    )
    new_room = models.Rooms(user_id, data["roomName"])
    models.DB.session.add(new_room)
    models.DB.session.commit()
    models.DB.session.refresh(new_room)
    models.DB.session.add(models.JoinedRooms(user_id, new_room.id))
    models.DB.session.commit()
    print("created new room:\n\t{}".format(new_room))
    emit_joined_rooms(flask.request.sid)

@socketio.on("join room request")
def on_join_room_request(data):
    print(
        "received a request to join room {} with this password: {}".format(
            data["roomId"], data["roomPassword"]
        )
    )
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()
    )
    room = (
        models.DB.session.query(models.Rooms)
        .filter_by(id=data["roomId"], password=data["roomPassword"])
        .first()
    )
    if room:
        models.DB.session.add(models.JoinedRooms(user_id, room.id))
    emit_joined_rooms(flask.request.sid)

@socketio.on("new google user login")
def accept_google_login(data):
    socketio.emit("login accepted", room=flask.request.sid)
    user = (
        models.DB.session.query(models.AuthUser)
        .filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data["email"])
        .first()
    )
    if not user:
        print("adding new user")
        models.DB.session.add(
            models.AuthUser(
                models.AuthUserType.GOOGLE, data["user"], data["email"], data["pic"]
            )
        )
        models.DB.session.commit()
        user = (
            models.DB.session.query(models.AuthUser)
            .filter_by(auth_type=models.AuthUserType.GOOGLE.value, email=data["email"])
            .first()
        )
    else:
        print("updating existing user")
        user.username = data["user"]
        user.picUrl = data["pic"]
    connection = (
        models.DB.session.query(models.CurrentConnections)
        .filter_by(sid=flask.request.sid)
        .first()
    )
    connection.user = user.id
    models.DB.session.commit()
    print("{} logged in".format(user.username))
    emit_joined_rooms(flask.request.sid)

@socketio.on("room entry request")
def on_room_entry_request(data):
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()
    )
    models.DB.session.add(models.EnteredRooms(user_id, data["roomId"]))
    models.DB.session.commit()
    socketio.emit("room entry accepted", room=flask.request.sid)
    flask_socketio.join_room(str(data["roomId"]))
    print("room entry accepted")
    emit_room_history(flask.request.sid)

    username = models.DB.session.query(models.AuthUser.username).filter_by(id=user_id).first()[0]
    if data['roomId'] not in roomTokens.keys():
        token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
        roomTokens[data['roomId']] = token
        token.add_grant(VideoGrant(room=data['roomId']))
        socketio.emit("token",
            {'tokens': token.to_jwt().decode(), 'room': str(data['roomId']), 'username': username})
    else:
        token = roomTokens[data['roomId']]
        token.identity=username
        socketio.emit("token",
            {'tokens': token.to_jwt().decode(), 'room': str(data['roomId']), 'username': username})

@socketio.on("leave room")
def accept_room_departure():
    disconnect_whiteboard(flask.request.sid)
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()[0]
    )
    room_id = (
        models.DB.session.query(models.EnteredRooms.room)
        .filter_by(user=user_id)
        .first()[0]
    )
    models.DB.session.query(models.EnteredRooms).filter_by(user=user_id).delete()
    models.DB.session.commit()
    socketio.emit(
        "left room",
        room=flask.request.sid,
    )
    flask_socketio.leave_room(str(room_id))
    print("user {} left room {}".format(user_id, room_id))
    emit_joined_rooms(flask.request.sid)
    emit_all_users(USERS_RECEIVED_CHANNEL, flask.request.sid)
    
@socketio.on("reset password")
def reset_room_password():
    print("Received password change request")
    client_sid = flask.request.sid
    room_id = get_room(client_sid)
    if client_sid == room_id:
        print("\tPassword not changed since sender is not in a room")
        return
    curr_conn_row = models.DB.session.query(models.CurrentConnections).filter_by(sid=client_sid).first()
    if curr_conn_row:
        client_user_id = curr_conn_row.user
    else:
        print("\tPassword not changed since sender is not connected")
        return
    room = models.DB.session.query(models.Rooms).filter_by(id=int(room_id)).first()
    if room:
        if client_user_id != room.creator:
            print("\tPassword not changed since sender is not room creator")
            return
    else:
        print("\tPassword not changed since room id is invalid")
        return
    room.password = models.GenerateCharacterPin(models.ROOM_PASSWORD_LENGTH)
    print("\tPassword for room {} changed to {}".format(room.id, room.password))
    models.DB.session.commit()
    emit_room_stats(client_sid)

@socketio.on("kick user request")
def kick_user(data):
    print(data)
    kick_target_id = data['kickedUserId']
    client_sid = flask.request.sid
    room_id = get_room(client_sid)
    print(
        "Received request to kick user {} from room {}".format(kick_target_id, room_id)
    )
    if client_sid == room_id:
        print("\tUser not kicked since room id was invalid")
        return
    client_user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=client_sid)
        .first()[0]
    )
    client_user_id = (
        models.DB.session.query(models.CurrentConnections)
        .filter_by(sid=client_sid).
        first().user
    )
    room = models.DB.session.query(models.Rooms).filter_by(id=room_id).first()
    if client_user_id != room.creator:
        print("\tUser not kicked since the request did not come from the room creator")
        return
    if kick_target_id == room.creator:
        print("\tUser not kicked since you can't kick the room creator")
        return
    kicked_entered_room_query = (
        models.DB.session.query(models.EnteredRooms)
        .filter_by(user=kick_target_id)
        .filter_by(room=room_id)
    )
    if kicked_entered_room_query.first():
        kicked_entered_room_query.delete()
    kicked_joined_room_query = (
        models.DB.session.query(models.JoinedRooms)
        .filter_by(user=kick_target_id)
        .filter_by(room=room_id)
    )
    if kicked_joined_room_query.first():
        kicked_joined_room_query.delete()
    kicked_current_connections_query = models.DB.session.query(
        models.CurrentConnections
    ).filter_by(user=kick_target_id)
    if kicked_current_connections_query.first():
        kicked_sid = kicked_current_connections_query.first().sid
        socketio.emit("kicked", {"roomId": room_id}, room=kicked_sid)
        socketio.emit('kicked', {'roomId': room_id}, room=str(kicked_sid))
    models.DB.session.commit()
    print("\tUser {} was kicked from room {}".format(kick_target_id, room_id))
    emit_all_users(USERS_RECEIVED_CHANNEL, flask.request.sid)

@socketio.on("i was kicked")
def simple_leave_room(data):
    disconnect_whiteboard(flask.request.sid)
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()[0]
    )
    room_id = data["roomId"]
    socketio.emit(
        "left room",
        room=flask.request.sid,
    )
    flask_socketio.leave_room(str(room_id))
    emit_joined_rooms(flask.request.sid)

@socketio.on("new message input")
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    user = {}
    user["sid"] = flask.request.sid
    user["room"] = get_room(
        flask.request.sid
    )  # TODO: get room_id from the sender request.sid
    user_id = (
        models.DB.session.query(models.CurrentConnections.user)
        .filter_by(sid=flask.request.sid)
        .first()[0]
    )
    user["username"] = (
        models.DB.session.query(models.AuthUser.username)
        .filter_by(id=user_id)
        .first()[0]
    )
    user["picUrl"] = (
        models.DB.session.query(models.AuthUser.picUrl)
        .filter_by(username=user["username"])
        .first()[0]
    )
    models.DB.session.add(
        models.Messages(user, user["username"] + ": " + data["message"])
    )
    models.DB.session.commit()
    emit_all_messages(flask.request.sid)

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
    emit_flashcards(flask.request.sid)

def emit_boards(my_sid):
    my_room = get_room(my_sid)
    to_send = []
    boards = models.DB.session.query(models.Whiteboards).filter_by(room=int(my_room))
    for board in boards:
        to_send.append({"name": board.name, "id": board.id})
    socketio.emit("got whiteboard", to_send, room=my_sid)

@socketio.on("make whiteboard")
def on_make_whiteboard(data):
    room = get_room(flask.request.sid)
    models.DB.session.add(models.Whiteboards(room, data["name"]))
    models.DB.session.commit()
    emit_boards(flask.request.sid)

@socketio.on("get whiteboards")
def on_get_whiteboard():
    emit_boards(flask.request.sid)

@socketio.on("remove whiteboard")
def on_remove_whiteboard(data):
    models.DB.session.query(models.Whiteboards).filter_by(id=data["id"]).delete()
    models.DB.session.commit()
    emit_boards(flask.request.sid)

@socketio.on("join whiteboard")
def on_join_whiteboard(data):
    my_leader = 1
    any_leader = (
        models.DB.session.query(models.WhiteboardConnections)
        .filter_by(whiteboard=data["id"], leader=1)
        .first()
    )
    if any_leader:
        my_leader = 0
        socketio.emit("force to save", room=any_leader.sid)
        print("make leader save", any_leader.sid)
    else:
        print("LOAD DEFAULT")
        save_num = (
            models.DB.session.query(models.Whiteboards)
            .filter_by(id=data["id"])
            .first()
            .save_num
        )
        socketio.emit(
            "load board",
            {
                "address": "https://ourstudybucket.s3.amazonaws.com/w{}s{}.png".format(
                    data["id"], save_num
                )
            },
            room=flask.request.sid,
        )
    models.DB.session.add(
        models.WhiteboardConnections(data["id"], flask.request.sid, my_leader)
    )
    models.DB.session.commit()
    flask_socketio.join_room("w{}".format((data["id"])))

@socketio.on("disconnect whiteboard")
def on_disconnect_whiteboard():
    disconnect_whiteboard(flask.request.sid)

def disconnect_whiteboard(my_sid):
    print("whiteboard disconnecting", my_sid)
    my_board = get_board(my_sid)
    try:
        int_board = int(my_board[1:])
        flask_socketio.leave_room(my_board, my_sid)
        models.DB.session.query(models.WhiteboardConnections).filter_by(
            sid=my_sid
        ).delete()
        models.DB.session.commit()
        any_leader = (
            models.DB.session.query(models.WhiteboardConnections)
            .filter_by(whiteboard=int_board, leader=1)
            .first()
        )
        if not any_leader:
            make_leader = (
                models.DB.session.query(models.WhiteboardConnections)
                .filter_by(whiteboard=int_board)
                .first()
            )
            if make_leader:
                print("promoting user")
                hold_query = models.DB.session.query(
                    models.WhiteboardConnections
                ).filter_by(id=make_leader.id)
                hold_query.update({models.WhiteboardConnections.leader: 1})
                models.DB.session.commit()
    except ValueError:
        print("not in whiteboard")

@socketio.on("drawing stroke input")
def on_drawing_stroke(data):
    room_id = get_board(flask.request.sid)
    socketio.emit("drawing stroke output", data, room=str(room_id))

@socketio.on("save")
def on_save(data):
    print("saving")
    do_save(data["blob"], get_board(flask.request.sid))

@socketio.on("forced save")
def on_forced_save(data):
    print("FORCED SAVE")
    board = get_board(flask.request.sid)
    save_num = do_save(data["blob"], board)
    socketio.emit(
        "load board",
        {
            "address": "https://ourstudybucket.s3.amazonaws.com/{}s{}.png".format(
                board, save_num
            )
        },
        room=board,
    )

def do_save(blob, board):
    s3_client = boto3.client(
        "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )
    try:
        entry = models.DB.session.query(models.Whiteboards).filter_by(id=int(board[1:]))
        old_num = entry.first().save_num
        new_num = old_num + 1
        s3_client.upload_fileobj(
            io.BytesIO(blob),
            "ourstudybucket",
            "{}s{}.png".format(board, new_num),
            ExtraArgs={"ACL": "public-read"},
        )
        if old_num > 0:
            s3_client.delete_object(
                Bucket="ourstudybucket", Key="{}s{}.png".format(board, old_num)
            )
        entry.update({models.Whiteboards.save_num: new_num})
        models.DB.session.commit()
    except ClientError as error:
        print(error)
    return new_num

@APP.route("/index.html")
def index():
    """ Return the index.html page on this route"""
    return flask.render_template("index.html")

@APP.route("/about.html")
@APP.route("/")
def about():
    """ Return the landing page at these routes"""
    return flask.render_template("about.html")

if __name__ == "__main__":
    database_init()
    clear_non_persistent_tables()
    socketio.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
