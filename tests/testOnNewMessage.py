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
KEY_DATA = 'data'
KEY_MESSAGE = 'message'

        
class testOnNewMessage(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_SID: '123456789ABCDEF',
                    KEY_DATA: 
                        
                        {
                    KEY_MESSAGE: 'hi',
                    },
                    
                },
              
                },
        ]
        
    @mock.patch('app.flask')
    def test_new_message_success(self, mock_flask):
            session = UnifiedAlchemyMagicMock()
            for test in self.success_test_params:
                mock_flask.request.sid = test[KEY_INPUT][KEY_SID]
                
                with mock.patch("models.DB.session", session):
                    session.add(models.CurrentConnections(test[KEY_INPUT][KEY_SID], 3))
                    session.add(models.AuthUser(models.AuthUserType.GOOGLE, 'nrw24', 'nrw24@njit.edu', 'pic'))
                    session.commit()
                    
                    app.on_new_message(test[KEY_INPUT][KEY_DATA])
            
               

if __name__ == "__main__":
    unittest.main()