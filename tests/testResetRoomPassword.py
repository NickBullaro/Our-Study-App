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

KEY_CURRENT_CONNECTIONS_DB = 'curr_conn'
KEY_ROOMS_DB = 'rooms_db'
KEY_SID = 'request_sid'
KEY_GET_ROOM_RETURN = 'get_room_rtn'
KEY_GENERATE_PIN_RETURN = 'not_so_random_pin'

KEY_HOLD_LIST = 'emitted'
KEY_HOLD_TYPE = 'captured_emit_type'
KEY_HOLD_EMIT_ROOM_STATS = 'emit_room_stats'
KEY_HOLD_PRINT = 'print'
KEY_PRINT_CONTENT = 'string'
KEY_ARGS = 'data'

def load_rooms_table(list_table):
    '''
    Loads a list of dictionaries into the mocked version of the current connections database
    '''
    for row in list_table:
        row_id = row['id']
        row_creator = row['creator']
        row_name = row['name']
        row_password = row['password']
        mockModels.Rooms(row_creator, row_name, roomPassword=row_password).add(row_id)

def export_rooms_table():
    '''
    returns the database as a list of dictionaries sorted in order of ascending id
    '''
    curr_db = mockModels.Rooms._db_dict.copy()
    db_list = []
    for row_id in curr_db:
        curr_row_dict ={}
        curr_row_dict['id'] = curr_db[row_id].id
        curr_row_dict['name'] = curr_db[row_id].name
        curr_row_dict['creator'] = curr_db[row_id].creator
        curr_row_dict['password'] = curr_db[row_id].password
        insertion_index = 0
        while insertion_index < len(db_list):
            if curr_row_dict['id'] < db_list[insertion_index]['id']:
                break
            insertion_index += 1
        db_list = db_list[:insertion_index] + [curr_row_dict] + db_list[insertion_index:]
    return db_list

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

class testEmitUsers(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            { # Test for a request from someone other than the room creator
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '0',
                        KEY_GENERATE_PIN_RETURN: 'QWER',
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 1,
                                'password': 'ASDF'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Received password change request"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tPassword not changed since sender is not room creator"
                            }],
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 1,
                                'password': 'ASDF'
                            }]
                    }
            },{ # Test for a request from the room creator
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '0',
                        KEY_GENERATE_PIN_RETURN: 'QWER',
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Received password change request"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tPassword for room 0 changed to QWER"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_EMIT_ROOM_STATS,
                                KEY_ARGS: '123456789ABCDEF'
                            }],
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'QWER'
                            }]
                    }
            },{ # Test if the user is not connected
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '0',
                        KEY_GENERATE_PIN_RETURN: 'QWER',
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456787654321'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Received password change request"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tPassword not changed since sender is not connected"
                            }],
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456787654321'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    }
            },{ # Test if the user is not in a room
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '123456789ABCDEF',
                        KEY_GENERATE_PIN_RETURN: 'QWER',
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Received password change request"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tPassword not changed since sender is not in a room"
                            }],
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    }
            },{ # Test if the room is somehow not valid
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '1',
                        KEY_GENERATE_PIN_RETURN: 'QWER',
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "Received password change request"
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_PRINT,
                                KEY_PRINT_CONTENT: "\tPassword not changed since room id is invalid"
                            }],
                        KEY_CURRENT_CONNECTIONS_DB:
                            [{
                                'id': 0,
                                'user': 15,
                                'sid': '123456789ABCDEF'
                            }],
                        KEY_ROOMS_DB:
                            [{
                                'id': 0,
                                'name': 'Test Room',
                                'creator': 15,
                                'password': 'ASDF'
                            }]
                    }
            }]
        self.hold = []
        
     def mock_print(self, *args):
        string = ''
        for arg in args:
            string += str(arg)
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_PRINT, KEY_PRINT_CONTENT: str(string)})

     def mock_emit_room_stats(self, client_sid):
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_EMIT_ROOM_STATS, KEY_ARGS: client_sid})

     @mock.patch('models.GenerateCharacterPin')
     @mock.patch('app.get_room')
     @mock.patch('app.flask')
     def test_emit_all_users_success(self, mock_flask, mock_get_room, mock_generate_pin):
        session = mockDBsession.MockSession()
        for test in self.success_test_params:
            self.hold = []
            mock_flask.request.sid = test[KEY_INPUT][KEY_SID]
            mock_get_room.return_value = test[KEY_INPUT][KEY_GET_ROOM_RETURN]
            mock_generate_pin.return_value = test[KEY_INPUT][KEY_GENERATE_PIN_RETURN]

            # Load the initial state of the tables
            mockModels.Rooms.reset_mock_database()
            load_rooms_table(test[KEY_INPUT][KEY_ROOMS_DB])
            mockModels.CurrentConnections.reset_mock_database()
            load_current_connections_table(test[KEY_INPUT][KEY_CURRENT_CONNECTIONS_DB])

            with mock.patch("models.DB.session", session):
                with mock.patch("app.emit_room_stats", self.mock_emit_room_stats):
                    with mock.patch("builtins.print", self.mock_print):
                        with mock.patch("models.Rooms", mockModels.Rooms):
                            with mock.patch("models.CurrentConnections", mockModels.CurrentConnections):
                                app.reset_room_password()

            # Verify that the table(s) state ageter execution matches what was expected
            createdTable = export_rooms_table()
            expectedTable = test[KEY_EXPECTED][KEY_ROOMS_DB]
            self.assertEqual(len(createdTable), len(expectedTable))
            for row_num in range(len(createdTable)):
                self.assertEqual(len(createdTable[row_num]), len(expectedTable[row_num]))
                for key in createdTable[row_num]:
                    self.assertTrue(key in expectedTable[row_num])
                    self.assertEqual(createdTable[row_num][key], expectedTable[row_num][key])
            createdTable = export_current_connections_table()
            expectedTable = test[KEY_EXPECTED][KEY_CURRENT_CONNECTIONS_DB]
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