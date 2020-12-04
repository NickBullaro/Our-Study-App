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

KEY_HOLD_LIST = 'emitted'
KEY_HOLD_TYPE = 'captured_emit_type'
KEY_HOLD_EMIT = 'emit'
KEY_HOLD_PRINT = 'print'
KEY_PRINT_CONTENT = 'string'
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
        curr_row_dict['auth_type'] = models.AuthUserType.matchEnum(curr_db[row_id].auth_type)
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
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "users: ['John Smith', 'Jill Smith']"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_EMIT,
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
            }
        ]
        self.hold = []

     def mock_emit(self, channel, data, room='default'):
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_EMIT, KEY_EMIT_ID: channel, KEY_DATA: data, KEY_EMIT_ROOM: room})
        
     def mock_print(self, *args):
        string = ''
        for arg in args:
            string += str(arg)
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_PRINT, KEY_PRINT_CONTENT: str(string)})

     def mock_get_room(self, client_sid):
         return 0

     @mock.patch('app.flask')
     def test_emit_all_users_success(self, mock_flash):
        session = mockDBsession.MockSession()
        for test in self.success_test_params:
            self.hold = []
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]

            # Load the initial state of the tables
            mockModels.EnteredRooms.reset_mock_database()
            load_entered_rooms_table(test[KEY_INPUT][KEY_ENTERED_ROOMS_DB])
            mockModels.AuthUser.reset_mock_database()
            load_users_table(test[KEY_INPUT][KEY_AUTH_USER_DB])

            with mock.patch("models.DB.session", session):
                with mock.patch("app.get_room", self.mock_get_room):
                    with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                        with mock.patch("models.EnteredRooms", mockModels.EnteredRooms):
                            with mock.patch("models.AuthUser", mockModels.AuthUser):
                                with mock.patch("builtins.print", self.mock_print):
                                    app.emit_all_users(test[KEY_INPUT][KEY_CHANNEL], test[KEY_INPUT][KEY_ROOM_ID])

            # Verify that the table(s) state ageter execution matches what was expected
            createdTable = export_entered_rooms_table()
            expectedTable = test[KEY_EXPECTED][KEY_ENTERED_ROOMS_DB]
            self.assertEqual(len(createdTable), len(expectedTable))
            for row_num in range(len(createdTable)):
                self.assertEqual(len(createdTable[row_num]), len(expectedTable[row_num]))
                for key in createdTable[row_num]:
                    self.assertTrue(key in expectedTable[row_num])
                    self.assertEqual(createdTable[row_num][key], expectedTable[row_num][key])
            createdTable = export_users_table()
            expectedTable = test[KEY_EXPECTED][KEY_AUTH_USER_DB]
            self.assertEqual(len(createdTable), len(expectedTable))
            for row_num in range(len(createdTable)):
                self.assertEqual(len(createdTable[row_num]), len(expectedTable[row_num]))
                for key in createdTable[row_num]:
                    self.assertTrue(key in expectedTable[row_num])
                    self.assertEqual(createdTable[row_num][key], expectedTable[row_num][key])

            # Verify that emits were as expected
            captured_emits = self.hold
            expected_emits = test[KEY_EXPECTED][KEY_HOLD_LIST]
            self.assertEqual(len(captured_emits), len(expected_emits))
            for i in range(len(captured_emits)):
                self.assertEqual(len(captured_emits[i]), len(expected_emits[i]))
                for key in captured_emits[i]:
                    self.assertTrue(key in expected_emits[i])
                    self.assertEqual(captured_emits[i][key], expected_emits[i][key])

    
if __name__ == "__main__":
    unittest.main()