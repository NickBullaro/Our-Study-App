import unittest
import unittest.mock as mock
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
from models import AuthUserType

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_SID = 'request_sid'
KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_ENTERED_ROOMS_DB = 'enter_room'
KEY_AUTH_USER_DB = 'auth_user'

class mockMockDBQuery():
    def __init__(self, mock_db_dict):
        self.db = mock_db_dict

class testOnDisconnect(unittest.TestCase):
    def setUp(self):
        self.test_on_disconnect_params = [
            {
                KEY_INPUT: 
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': 0,
                            'sid': '123456789ABCDEF'
                        },{
                            'id': 1,
                            'user': 1,
                            'sid': '000000000000000'
                        }],
                        KEY_ENTERED_ROOMS_DB: [{
                            'id': 0,
                            'user': 0,
                            'room': 0
                        },{
                            'id': 1,
                            'user': 1,
                            'room': 0
                        }],
                        KEY_AUTH_USER_DB: [{
                            'id': 0,
                            'auth_type': AuthUserType.GOOGLE.value,
                            'username': 'John Smith',
                            'email': 'jSmith@gmail.com',
                            'pirUrl': 'www.google.com'
                        },{
                            'id': 1,
                            'auth_type': AuthUserType.GOOGLE.value,
                            'username': 'Tom Ato',
                            'email': 'fakeEmail@gmail.com',
                            'pirUrl': 'www.google.com'
                        }],
                    }
            }]
    pass

if __name__ == "__main__":
    unittest.main()