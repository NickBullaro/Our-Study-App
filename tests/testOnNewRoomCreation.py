import unittest
import unittest.mock as mock
import os, sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_RESPONSE = 'response'

KEY_ANSWER = 'answer'
KEY_QUESTION = 'question'
KEY_ROOM = 'room'
KEY_DATA = 'data'
KEY_CHANNEL = 'channel'
KEY_ROOM_NAME = 'roomName'

KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_SID = 'request_sid'
KEY_NUM_ADDITIONS =  'times_in_database'

KEY_EMIT_ID = 'emit_id'
KEY_EMIT_ROOM = 'room'

        
class testNewRoomCreation(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_EMIT_ID: 'cards',
                    KEY_DATA: {
                        KEY_ROOM_NAME : 'roomer'
                        
                    },
                    KEY_SID: '123456789ABCDEF',
                    
                    },
            
                },
        ]
 
        self.hold = ''
            
     def mock_emit(self, sid, data, room='default'):
        self.hold = {KEY_EMIT_ID: sid, KEY_DATA: data, KEY_EMIT_ROOM: room}
 
     @mock.patch('app.flask')
     def test_new_room_creation_success(self, mock_flash):
        session = UnifiedAlchemyMagicMock()
        for test in self.success_test_params:
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
              
                session.add(models.CurrentConnections(test[KEY_INPUT][KEY_SID], 1))
                session.add(models.JoinedRooms(1,2))
                session.commit()
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    print(app.on_new_room_creation(test[KEY_INPUT][KEY_DATA]))
        
               

    
if __name__ == "__main__":
    unittest.main()