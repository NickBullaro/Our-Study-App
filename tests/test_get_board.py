'''Tests get_board '''
import unittest
import unittest.mock as mock
import os
import sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

#import is need to be placed after this statement so circleci can run test correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
import models


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_SID = "request_sid"
KEY_DATA = "data"
KEY_EMIT_ID = "id"
KEY_EMIT_ROOM = "room"
KEY_CONNECTION = "connection"


class TestGetBoard(unittest.TestCase):
    def setUp(self):
        self.test_get_board_params = [
            {
                KEY_INPUT: {
                    KEY_SID:5,
                    KEY_CONNECTION:[2,5,0]
                },
                KEY_EXPECTED: "w2",
            }
        ]
        self.hold = {}

    def mock_emit(self, my_id, data, room="default"):
        self.hold = {KEY_EMIT_ID: my_id, KEY_DATA: data, KEY_EMIT_ROOM: room}

    @mock.patch("app.flask")
    def test_app_get_board(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_get_board_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("models.DB.session", session):
                    session.add(models.WhiteboardConnections(*test[KEY_INPUT][KEY_CONNECTION]))
                    session.commit()
                    self.assertEqual(app.get_board(test[KEY_INPUT][KEY_SID]), test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()