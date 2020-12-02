'''Tests on_drawing_stroke '''
import unittest
import unittest.mock as mock
import os
import sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

#import is need to be placed after this statement so circleci can run test correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_SID = "request_sid"
KEY_CURRENT_CONNECTIONS_DB = "curr_con"
KEY_NUM_ADDITIONS = "times_in_database"
KEY_DATA = "data"
KEY_EMIT_ID = "id"
KEY_EMIT_ROOM = "room"


class TestOnDrawingStroke(unittest.TestCase):
    def setUp(self):
        self.test_on_stroke_params = [
            {
                KEY_INPUT: {
                    KEY_SID: "123456789ABCDEF",
                    KEY_DATA: {
                        "oldx": 0,
                        "oldy": 0,
                        "newx": 0,
                        "newy": 0,
                        "color": "#000000",
                    },
                },
                KEY_EXPECTED: {
                    KEY_EMIT_ID: "drawing stroke output",
                    KEY_DATA: {
                        "oldx": 0,
                        "oldy": 0,
                        "newx": 0,
                        "newy": 0,
                        "color": "#000000",
                    },
                    KEY_EMIT_ROOM: "123456789ABCDEF",
                },
            },
            {
                KEY_INPUT: {
                    KEY_SID: "12345AAAAA54321",
                    KEY_DATA: {
                        "oldx": 56,
                        "oldy": 85,
                        "newx": 21,
                        "newy": 20,
                        "color": "#660000",
                    },
                },
                KEY_EXPECTED: {
                    KEY_EMIT_ID: "drawing stroke output",
                    KEY_DATA: {
                        "oldx": 56,
                        "oldy": 85,
                        "newx": 21,
                        "newy": 20,
                        "color": "#660000",
                    },
                    KEY_EMIT_ROOM: "12345AAAAA54321",
                },
            },
        ]
        self.hold = {}

    def mock_emit(self, my_id, data, room="default"):
        self.hold = {KEY_EMIT_ID: my_id, KEY_DATA: data, KEY_EMIT_ROOM: room}
    
    def mock_get_room(self, client_sid):
        return client_sid

    @mock.patch("app.flask")
    def test_app_on_connect(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_stroke_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("app.get_room", self.mock_get_room):
                    app.on_drawing_stroke(test[KEY_INPUT][KEY_DATA])

            self.assertDictEqual(self.hold, test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()
