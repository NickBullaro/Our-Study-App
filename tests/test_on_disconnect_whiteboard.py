'''Tests on_disconnect_whiteboard '''
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


class TestOnDisconnectWhiteboard(unittest.TestCase):
    def setUp(self):
        self.test_on_disconnect_whiteboard_params = [
            {
                KEY_INPUT: {
                    KEY_SID:5,
                    KEY_CONNECTION:[[2,5,1],[2,4,0]]
                },
                KEY_EXPECTED: "promoting user",
            }
        ]
        self.hold = ""

    def mock_print(self, my_string, param):
        self.hold = my_string
        
    def mock_leave_group(self, param, other_param):
        pass

    @mock.patch("app.flask")
    @mock.patch("builtins.print")
    def test_on_disconnect_whiteboard_board(self, mocked_print, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_disconnect_whiteboard_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.leave_room",self.mock_leave_group):
                with mock.patch("models.DB.session", session):
                    for connect in test[KEY_INPUT][KEY_CONNECTION]:
                        temp_row = models.WhiteboardConnections(*connect)
                        temp_row.id = 1
                        session.add(temp_row)
                        session.commit()
                    app.on_disconnect_whiteboard()
                    mocked_print.assert_called_with(test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()