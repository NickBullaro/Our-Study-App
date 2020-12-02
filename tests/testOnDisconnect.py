import unittest
import unittest.mock as mock
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
import models
from models import AuthUserType
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_SID = 'request_sid'
KEY_MOCK_DATABASE_CALLS = 'mock call responses'

class testOnDisconnect(unittest.TestCase):
    def append_emit_list(self, new_dict):
        self.emit_list.append(new_dict)

    def mock_print(self, message):
        self.append_emit_list({"opp": "print"})

    def mock_emit_all_users(self, message, room):
        self.append_emit_list({"opp": "emit"})
    
    @staticmethod
    def mock_get_room(client_sid):
        return 0
    
    def setUp(self):
        self.emit_list = []
        self.test_on_disconnect_params = [
            {
                KEY_INPUT: 
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_MOCK_DATABASE_CALLS: 
                            [(
                                [mock.call.query(models.CurrentConnections),
                                mock.call.filter_by(sid='123456789ABCDEF'),
                                mock.call.first()]
                                ,
                                models.CurrentConnections('123456789ABCDEF', 0)
                            ),
                            (
                                [mock.call.query(models.EnteredRooms),
                                mock.call.filter_by(user=0),
                                mock.call.delete()]
                                ,
                                self.append_emit_list({"opp": "deleteEntered"})
                            ),
                            (
                                [mock.call.query(models.AuthUser),
                                mock.call.filter_by(id=0),
                                mock.call.first()]
                                ,
                                models.AuthUser(models.AuthUserType.GOOGLE, 'user1', 'usr@gmail.com', 'www.google.com')
                            ),
                            (
                                [mock.call.delete(models.AuthUser)]
                                ,
                                self.append_emit_list({"opp": "deleteAuth"})
                            )]
                    },
                KEY_EXPECTED:
                    [
                        {"opp": "deleteEntered"},
                        {"opp": "deleteAuth"},
                        {"opp": "print"}
                    ]
            }]

    @mock.patch('app.flask')
    def test_app_on_disconnect(self, mocked_flask):
        for test in self.test_on_disconnect_params:
            session = UnifiedAlchemyMagicMock()
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch('models.DB.session', session):
                session.add(models.CurrentConnections(test[KEY_INPUT][KEY_SID],1))
                session.add(models.AuthUser(models.AuthUserType.GOOGLE, 'nrw41', 'meail', 'pciina'))
                session.commit()
                #with mock.patch('app.print', self.mock_print):
                #    with mock.patch('app.emit_all_users', self.mock_emit_all_users):
                with mock.patch('app.get_room', self.mock_get_room):
                   app.on_disconnect()
            
            self.assertEqual(len(self.emit_list) + 1,len(test[KEY_EXPECTED]))
            for i in range(len(self.emit_list)):
                self.assertEqual(self.emit_list[i]['opp'], test[KEY_EXPECTED][i]['opp'])
            

if __name__ == "__main__":
    unittest.main()