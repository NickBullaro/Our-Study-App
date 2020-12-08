'''Tests emit_boards '''
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
BOARD_DATA = "board"


class TestEmitBoards(unittest.TestCase):
    def setUp(self):
        self.test_emit_boards_params = [
            {
                KEY_INPUT: {
                    KEY_SID:1,
                    BOARD_DATA:[1,"brett"]
                },
                KEY_EXPECTED: {
                    KEY_EMIT_ID: "got whiteboard",
                    KEY_DATA:[{"id":None,"name":"brett"}],
                    KEY_EMIT_ROOM: 1
                },
            }
        ]
        self.hold = {}

    def mock_emit(self, my_id, data, room="default"):
        self.hold = {KEY_EMIT_ID: my_id, KEY_DATA: data, KEY_EMIT_ROOM: room}

    @mock.patch("app.flask")
    def test_app_emit_boards(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_emit_boards_params:
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("models.DB.session", session):
                    session.add(models.Whiteboards(*test[KEY_INPUT][BOARD_DATA]))
                    session.commit()
                    app.emit_boards(test[KEY_INPUT][KEY_SID])

            self.assertDictEqual(self.hold, test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()