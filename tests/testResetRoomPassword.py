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
        
class testResetPassword(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_EMIT_ID: "sending room data",
                    KEY_DATA:  {KEY_ROOM : 2},
                    KEY_SID: '123456789ABCDEF'
                    },
           
                },
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT :
                    {
                    KEY_EMIT_ID: "sending room data",
                    KEY_DATA:  {KEY_ROOM : 2},
                    KEY_SID: 0
                    }
            }
            
            ]
 
        self.hold = ''
            
     def mock_emit(self, sid, data, room='default'):
        self.hold = {KEY_EMIT_ID: sid, KEY_DATA: data, KEY_EMIT_ROOM: room}
    
     def mock_get_room(self,client_sid): 
        return 0 
        
     def mock_get_room_fail(self, client_sid):
         return 2
     @mock.patch('app.flask')
     def test_reset_password_success(self, mock_flash):
        session = UnifiedAlchemyMagicMock()
        for test in self.success_test_params:
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    session.add(models.AuthUser(models.AuthUserType.GOOGLE, 'nrw', 'fakeemail', 'picr'  ))
                    session.add(models.CurrentConnections(test[KEY_INPUT][KEY_SID], 1))
                    session.add(models.Rooms(1, 'roomt'))
                    session.add(models.EnteredRooms(1, 1))
                    session.commit()
                    with mock.patch('app.get_room', self.mock_get_room):
                        app.reset_room_password()
                        
     @mock.patch('app.flask')
     def test_reset_password_failure(self, mock_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.failure_test_params:
            mock_flask.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    session.add(models.AuthUser(models.AuthUserType.GOOGLE, 'nrw', 'fakeemail', 'picr'  ))
                    session.add(models.AuthUser(models.AuthUserType.GOOGLE, 'nrw3', 'fakeemail21', 'pi21cr'  ))
                    session.add(models.CurrentConnections(test[KEY_INPUT][KEY_SID], 1))
                    session.add(models.Rooms(1, 'roomt'))
                    session.add(models.Rooms(3,'room'))
                    session.add(models.EnteredRooms(2, 2))
                    session.commit()
                    with mock.patch('app.get_room', self.mock_get_room):
                        app.reset_room_password()
        
               

    
if __name__ == "__main__":
    unittest.main()