import unittest
import unittest.mock as mock
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
import models
import mockDBsession
import mockModels

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_SID = 'request_sid'
KEY_GET_ROOM_RETURN = 'get_room_rtn'
KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_AUTH_USER_DB = 'auth_usr'
KEY_MESSAGES_DB = 'msgs'
KEY_DATA = 'function_input'

KEY_HOLD_LIST = 'emitted'
KEY_HOLD_TYPE = 'captured_emit_type'
KEY_HOLD_PRINT = 'print'
KEY_PRINT_CONTENT = 'string'
KEY_HOLD_EMIT_ALL_MESSAGES = 'emit_all_messages'
KEY_ARGS = 'args'

def load_current_connections_table(list_curr_conn):
    '''
    Loads a list of dictionaries into the mocked version of the current connections database
    '''
    for row in list_curr_conn:
        row_id = row['id']
        row_sid = row['sid']
        row_user = row['user']
        mockModels.CurrentConnections(row_sid, row_user).add(row_id)

def export_current_connections_table():
    '''
    returns the database as a list of dictionaries sorted in order of ascending id
    '''
    curr_db = mockModels.CurrentConnections._db_dict.copy()
    db_list = []
    for row_id in curr_db:
        curr_row_dict ={}
        curr_row_dict['id'] = curr_db[row_id].id
        curr_row_dict['sid'] = curr_db[row_id].sid
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

def load_messages_table(list_curr_conn):
    '''
    Loads a list of dictionaries into the mocked version of the current connections database
    '''
    for row in list_curr_conn:
        row_id = row['id']
        row_message = row['message']
        row_user = {}
        row_user['sid'] = row['sid']
        row_user['username'] = row['username']
        row_user['room'] = row['room']
        row_user['picUrl'] = row['picUrl']
        mockModels.Messages(row_user, row_message).add(row_id)

def export_messages_table():
    '''
    returns the database as a list of dictionaries sorted in order of ascending id
    '''
    curr_db = mockModels.Messages._db_dict.copy()
    db_list = []
    for row_id in curr_db:
        curr_row_dict ={}
        curr_row_dict['id'] = curr_db[row_id].id
        curr_row_dict['sid'] = curr_db[row_id].sid
        curr_row_dict['username'] = curr_db[row_id].username
        curr_row_dict['room'] = curr_db[row_id].room
        curr_row_dict['picUrl'] = curr_db[row_id].picUrl
        curr_row_dict['message'] = curr_db[row_id].message
        insertion_index = 0
        while insertion_index < len(db_list):
            if curr_row_dict['id'] < db_list[insertion_index]['id']:
                break
            insertion_index += 1
        db_list = db_list[:insertion_index] + [curr_row_dict] + db_list[insertion_index:]
    return db_list

class testOnNewMessage(unittest.TestCase):
    def setUp(self):
        self.test_params = [
            {   
                KEY_INPUT:  
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '0',
                        KEY_DATA: {'message': 'hello world'},
                        KEY_CURRENT_CONNECTIONS_DB: [{
                                'id': 0,
                                'user': 0,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_AUTH_USER_DB:
                            [{
                                'id': 0,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'John Smith',
                                'email': 'jsmith@gmail.com',
                                'picUrl': ''
                            }],
                        KEY_MESSAGES_DB:
                            [{
                                'id': 0,
                                'sid': '123456789ABCDEF',
                                'room': '0',
                                'picUrl': '',
                                'username': 'John Smith',
                                'message': 'John Smith: knock knock'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_CURRENT_CONNECTIONS_DB: [{
                                'id': 0,
                                'user': 0,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_AUTH_USER_DB:
                            [{
                                'id': 0,
                                'auth_type': models.AuthUserType.GOOGLE,
                                'username': 'John Smith',
                                'email': 'jsmith@gmail.com',
                                'picUrl': ''
                            }],
                        KEY_MESSAGES_DB:
                            [{
                                'id': 0,
                                'sid': '123456789ABCDEF',
                                'room': '0',
                                'picUrl': '',
                                'username': 'John Smith',
                                'message': 'John Smith: knock knock'
                            },{
                                'id': 1,
                                'sid': '123456789ABCDEF',
                                'room': '0',
                                'picUrl': '',
                                'username': 'John Smith',
                                'message': 'John Smith: hello world'
                            }],
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Got an event for new message input"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tmessage added to message history"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_EMIT_ALL_MESSAGES,
                                KEY_ARGS: "123456789ABCDEF"
                            }]
                    }
            }]
        self.hold = []
        
    def mock_print(self, *args):
        string = ''
        for arg in args:
            string += str(arg)
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_PRINT, KEY_PRINT_CONTENT: str(string)})

    def mock_emit_all_messages(self, client_sid):
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_EMIT_ALL_MESSAGES, KEY_ARGS: client_sid})

    @mock.patch('app.get_room')
    @mock.patch('app.flask')
    def test_app_on_new_message(self, mocked_flask, mocked_get_room):
        session = mockDBsession.MockSession()
        for test in self.test_params:
            mockModels.CurrentConnections.reset_mock_database()
            load_current_connections_table(test[KEY_INPUT][KEY_CURRENT_CONNECTIONS_DB])
            mockModels.AuthUser.reset_mock_database()
            load_users_table(test[KEY_INPUT][KEY_AUTH_USER_DB])
            mockModels.Messages.reset_mock_database()
            load_messages_table(test[KEY_INPUT][KEY_MESSAGES_DB])
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            mocked_get_room.return_value = test[KEY_INPUT][KEY_GET_ROOM_RETURN]
            self.hold = []

            with mock.patch('models.DB.session', session):
                with mock.patch('models.CurrentConnections', mockModels.CurrentConnections):
                    with mock.patch('models.AuthUser', mockModels.AuthUser):
                        with mock.patch('models.Messages', mockModels.Messages):
                            with mock.patch('builtins.print', self.mock_print):
                                with mock.patch('app.emit_all_messages', self.mock_emit_all_messages):
                                    app.on_new_message(test[KEY_INPUT][KEY_DATA])

            # Verify that the table(s) state after execution matches what was expected
            createdTable = export_current_connections_table()
            expectedTable = test[KEY_EXPECTED][KEY_CURRENT_CONNECTIONS_DB]
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
            createdTable = export_messages_table()
            expectedTable = test[KEY_EXPECTED][KEY_MESSAGES_DB]
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