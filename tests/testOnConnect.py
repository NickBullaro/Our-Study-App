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
KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_NUM_ADDITIONS = 'times_in_database'

class testOnConnect(unittest.TestCase):
    def setUp(self):
        self.test_on_connect_params = [
            {   
                KEY_INPUT:  
                    {
                        KEY_SID: '123456789ABCDEF'
                    },
                KEY_EXPECTED:
                    {
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': None,
                            'sid': '123456789ABCDEF'
                        }],
                        KEY_NUM_ADDITIONS: 1
                    }
            },
            {   
                KEY_INPUT:  
                    {
                        KEY_SID: '123456787654321'
                    },
                KEY_EXPECTED:
                    {
                        KEY_CURRENT_CONNECTIONS_DB: [{
                            'id': 0,
                            'user': None,
                            'sid': '123456787654321'
                        }],
                        KEY_NUM_ADDITIONS: 1
                    }
            }]

    @mock.patch('app.flask')
    def test_app_on_connect(self, mocked_flask):
        session = UnifiedAlchemyMagicMock()
        for test in self.test_on_connect_params:
            mocked_flask.request.sid = test[KEY_INPUT][KEY_SID]
            num_in_database = session.query(models.CurrentConnections).count()
            with mock.patch('models.DB.session', session):
                app.on_connect()
            
            num_added_to_database = session.query(models.CurrentConnections).count() - num_in_database

            self.assertEqual(num_added_to_database, test[KEY_EXPECTED][KEY_NUM_ADDITIONS])

if __name__ == "__main__":
    unittest.main()