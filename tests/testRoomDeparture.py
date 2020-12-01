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

KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_SID = 'request_sid'
KEY_NUM_ADDITIONS =  'times_in_database'

KEY_EMIT_ID = 'emit_id'
KEY_EMIT_ROOM = 'room'


class MockLeave:
    def __call__(self, r):
        print('selfish')
        
    def __init__(self, room):
        self.room = room
        
class testRoomDeparture(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_EMIT_ID: 'cards',
                    KEY_DATA: [{'question' : 'question', 'answer': 'answer'}],
                    KEY_SID: '123456789ABCDE0'
                    },
                KEY_EXPECTED: ('2+2', 4, '123456789ABCDEF') 
                },
        ]
 
        self.hold = ''
        self.users = [models.EnteredRooms(1,1), models.EnteredRooms(2,3)]
        
     def mock_emit(self, sid, data='', room='default'):
        self.hold = {KEY_EMIT_ID: sid, KEY_DATA: data, KEY_EMIT_ROOM: room}
  
     def mock_leave_room(self):
         temp = self.users[1:]
         self.users = temp
         return MockLeave(1)

     def mocked_cards(self):
         return [MockedFlashCards('question', 'answer', '123456789ABCDEF')]
         
     '''  @mock.patch('app.flask')
     def test_room_departure_success(self, mock_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.success_test_params:
            mock_flask.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                session.add(models.CurrentConnections(mock_flask.request.sid, 1))
                session.add(models.EnteredRooms(1,2))
                session.commit()
               
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    with mock.patch('flask_socketio.leave_room', self.mock_leave_room()):
                        app.accept_room_departure()
    
               '''

    
if __name__ == "__main__":
    unittest.main()