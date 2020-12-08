'''Tests on_join_whiteboard '''
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


class TestOnJoinWhiteboard(unittest.TestCase):
    def setUp(self):
        self.test_on_join_whiteboard_params = [
            {
                KEY_INPUT: {
                    KEY_SID:1,
                    KEY_DATA:{"id":5,"name":"chett"},
                    BOARD_DATA:{"id":5,"room":1,"name":"chett","save_num":7}
                },
                KEY_EXPECTED: {
                    KEY_EMIT_ID: "load board",
                    KEY_DATA:{"address":"https://ourstudybucket.s3.amazonaws.com/w5s7.png"},
                    KEY_EMIT_ROOM: 1
                },
            }
        ]
        self.test_on_join_whiteboard_other = [
            {
                KEY_INPUT: {
                    KEY_SID:1,
                    KEY_DATA:{"id":5,"name":"chett"},
                    BOARD_DATA:[5,5,1]
                },
                KEY_EXPECTED: {
                    KEY_EMIT_ID: "force to save",
                    KEY_DATA:None,
                    KEY_EMIT_ROOM: 5
                },
            }
        ]
        self.hold = {}

    def mock_emit(self, my_id, data=None, room="default"):
        self.hold = {KEY_EMIT_ID: my_id, KEY_DATA: data, KEY_EMIT_ROOM: room}
        
    def mock_join_room(self,room):
        pass

    @mock.patch("app.flask")
    def test_on_join_whiteboard(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_join_whiteboard_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("flask_socketio.join_room", self.mock_join_room):  
                    with mock.patch("models.DB.session", session):
                        temp_row=models.Whiteboards(test[KEY_INPUT][BOARD_DATA]["room"],test[KEY_INPUT][BOARD_DATA]["name"])
                        temp_row.id=test[KEY_INPUT][BOARD_DATA]["id"]
                        temp_row.save_num=test[KEY_INPUT][BOARD_DATA]["save_num"]
                        session.add(temp_row)
                        
                        session.commit()
                        app.on_join_whiteboard(test[KEY_INPUT][KEY_DATA])

            self.assertDictEqual(self.hold, test[KEY_EXPECTED])
            
    @mock.patch("app.flask")
    def test_on_join_whiteboard_other(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_join_whiteboard_other:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                with mock.patch("flask_socketio.join_room", self.mock_join_room):  
                    with mock.patch("models.DB.session", session):
                        temp_row=models.WhiteboardConnections(*test[KEY_INPUT][BOARD_DATA])
                        temp_row.id = 1
                        session.add(temp_row)
                        
                        session.commit()
                        app.on_join_whiteboard(test[KEY_INPUT][KEY_DATA])

            self.assertDictEqual(self.hold, test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()