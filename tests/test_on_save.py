'''Tests on_forced_save'''
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
KEY_BOARD = "board"
KEY_CONNECTION = "connect"


class on_forced_save(unittest.TestCase):
    def setUp(self):
        self.test_on_forced_save_params = [
            {
                KEY_INPUT: {
                    KEY_SID:666,
                    KEY_BOARD:[666,"hello",666],
                    KEY_CONNECTION:[666,666,1]
                },
                KEY_EXPECTED: "saving",
            }
        ]
        self.hold = {}

    def mock_emit(self, my_id, data, room="default"):
        self.hold = {KEY_EMIT_ID: my_id, KEY_DATA: data, KEY_EMIT_ROOM: room}

    @mock.patch("app.flask")
    @mock.patch("builtins.print")
    def test_app_on_forced_save(self, mocked_print, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_forced_save_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("models.DB.session", session):
                    temp_row=models.Whiteboards(*test[KEY_INPUT][KEY_BOARD][:2])
                    temp_row.save_num = test[KEY_INPUT][KEY_BOARD][2]
                    session.add(temp_row)
                    session.add(models.WhiteboardConnections(*test[KEY_INPUT][KEY_CONNECTION]))
                    session.commit()
                    app.on_save({"blob":bytes([1,5,2,5,3,2,1])})
                mocked_print.assert_called_with(test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()