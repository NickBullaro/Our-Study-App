from dotenv import load_dotenv
import os
import flask
import flask_socketio
import flask_sqlalchemy

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

if __name__ == "__main__":
    db_init()
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )