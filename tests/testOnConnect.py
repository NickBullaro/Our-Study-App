import unittest
import unittest.mock as mock
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
import mockDBsession
import mockModels

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_SID = 'request_sid'
KEY_CURRENT_CONNECTIONS_DB = 'curr_con'

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

class testOnConnect(unittest.TestCase):
    def setUp(self):
        self.test_on_connect_params = [
            {   
                KEY_INPUT:  
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_CURRENT_CONNECTIONS_DB: []
                    },
                KEY_EXPECTED:
                    {
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': None,
                            'sid': '123456789ABCDEF'
                        }],
                    }
            },
            {   
                KEY_INPUT:  
                    {
                        KEY_SID: '123456787654321',
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': None,
                            'sid': '123456789ABCDEF'
                        }]
                    },
                KEY_EXPECTED:
                    {
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': None,
                            'sid': '123456789ABCDEF'
                        }, {
                            'id': 1,
                            'user': None,
                            'sid': '123456787654321'
                        }],
                    }
            }]

    @mock.patch('app.flask')
    def test_app_on_connect(self, mocked_flask):
        session = mockDBsession.MockSession()
        for test in self.test_on_connect_params:
            mockModels.CurrentConnections.reset_mock_database()
            load_current_connections_table(test[KEY_INPUT][KEY_CURRENT_CONNECTIONS_DB])
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            with mock.patch('models.DB.session', session):
                with mock.patch('models.CurrentConnections', mockModels.CurrentConnections):
                    app.on_connect()

            createdTable = export_current_connections_table()
            expectedTable = test[KEY_EXPECTED][KEY_CURRENT_CONNECTIONS_DB]
            self.assertEqual(len(createdTable), len(expectedTable))
            for row_num in range(len(createdTable)):
                self.assertEqual(len(createdTable[row_num]), len(expectedTable[row_num]))
                for key in createdTable[row_num]:
                    self.assertTrue(key in expectedTable[row_num])
                    self.assertEqual(createdTable[row_num][key], expectedTable[row_num][key])

if __name__ == "__main__":
    unittest.main()