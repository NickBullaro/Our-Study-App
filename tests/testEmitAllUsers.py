import unittest
import unittest.mock as mock
import os, sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models
import mockModels
import mockDBsession


KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_RESPONSE = 'response'

KEY_ROOM_ID = 'room_id'
KEY_CHANNEL = 'channel'
KEY_ENTERED_ROOMS_DB = 'enter_rm'
KEY_AUTH_USER_DB = 'auth_usr'
KEY_SID = 'request_sid'

KEY_EMIT_LIST = 'emitted'

KEY_EMIT_ID = 'emit_id'
KEY_DATA = 'data'
KEY_EMIT_ROOM = 'room'

def load_entered_rooms_table(list_table):
    '''
    Loads a list of dictionaries into the mocked version of the current connections database
    '''
    for row in list_table:
        row_id = row['id']
        row_room = row['room']
        row_user = row['user']
        mockModels.EnteredRooms(row_user, row_room).add(row_id)

def export_entered_rooms_table():
    '''
    returns the database as a list of dictionaries sorted in order of ascending id
    '''
    curr_db = mockModels.EnteredRooms._db_dict.copy()
    db_list = []
    for row_id in curr_db:
        curr_row_dict ={}
        curr_row_dict['id'] = curr_db[row_id].id
        curr_row_dict['room'] = curr_db[row_id].room
        curr_row_dict['user'] = curr_db[row_id].user
        insertion_index = 0
        while insertion_index < len(db_list):
            if curr_row_dict['id'] < db_list[insertion_index]['id']:
                break
            insertion_index += 1
        db_list = db_list[:insertion_index] + [curr_row_dict] + db_list[insertion_index:]
    return db_list

def load_users_table(list_table):
    '''
    Loads a list of dictionaries into the mocked version of the current connections database
    '''
    for row in list_table:
        row_id = row['id']
        row_auth = row['auth_type']
        row_name = row['username']
        row_email = row['email']
        row_pic = row['picUrl']
        mockModels.AuthUser(row_auth, row_name, row_email, row_pic).add(row_id)

def export_users_table():
    '''
    returns the database as a list of dictionaries sorted in order of ascending id
    '''
    curr_db = mockModels.AuthUser._db_dict.copy()
    db_list = []
    for row_id in curr_db:
        curr_row_dict ={}
        curr_row_dict['id'] = curr_db[row_id].id
        curr_row_dict['auth_type'] = curr_db[row_id].auth_type
        curr_row_dict['username'] = curr_db[row_id].username
        curr_row_dict['email'] = curr_db[row_id].email
        curr_row_dict['picUrl'] = curr_db[row_id].picUrl
        insertion_index = 0
        while insertion_index < len(db_list):
            if curr_row_dict['id'] < db_list[insertion_index]['id']:
                break
            insertion_index += 1
        db_list = db_list[:insertion_index] + [curr_row_dict] + db_list[insertion_index:]
    return db_list

class testEmitUsers(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_CHANNEL: 'users received',
                        KEY_ROOM_ID: 0,
                        KEY_ENTERED_ROOMS_DB:
                            [{
                                'id': 0,
                                'room': 0,
                                'user': 0
                            },{
                                'id': 1,
                                'room': 0,
                                'user': 1
                            }],
                        KEY_AUTH_USER_DB:
                            [{
                                'id': 0,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'John Smith',
                                'email': 'jsmith@gmail.com',
                                'picUrl': ''
                            },{
                                'id': 1,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'Jill Smith',
                                'email': 'jill_s@gmail.com',
                                'picUrl': ''
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_EMIT_LIST:
                            [{
                                KEY_EMIT_ID: 'users received',
                                KEY_DATA: 
                                    {
                                        'all_users': ['John Smith', 'Jill Smith'],
                                        'all_user_pics': ['', ''],
                                        'all_user_ids': [0, 1]
                                    },
                                KEY_EMIT_ROOM: 0
                            }],
                        KEY_ENTERED_ROOMS_DB:
                            [{
                                'id': 0,
                                'room': 0,
                                'user': 0
                            },{
                                'id': 1,
                                'room': 0,
                                'user': 1
                            }],
                        KEY_AUTH_USER_DB:
                            [{
                                'id': 0,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'John Smith',
                                'email': 'jsmith@gmail.com',
                                'picUrl': ''
                            },{
                                'id': 1,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'Jill Smith',
                                'email': 'jill_s@gmail.com',
                                'picUrl': ''
                            }]
                    }
            },
        ]
 
        self.hold = []
            
     def mock_emit(self, channel, data, room='default'):
        self.hold.append({KEY_EMIT_ID: channel, KEY_DATA: data, KEY_EMIT_ROOM: room})
    
     def mock_get_room(self, client_sid):
         return 0

     @mock.patch('app.flask')
     def test_emit_all_users_success(self, mock_flash):
        session = mockDBsession.MockSession()
        for test in self.success_test_params:
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                with mock.patch("app.get_room", self.mock_get_room):
                    with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                        with mock.patch("models.EnteredRooms", mockModels.EnteredRooms):
                            with mock.patch("models.AuthUser", mockModels.AuthUser):
                                app.emit_all_users(test[KEY_INPUT][KEY_CHANNEL], test[KEY_INPUT][KEY_ROOM_ID])
        
            

    
if __name__ == "__main__":
    unittest.main()