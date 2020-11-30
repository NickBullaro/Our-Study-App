import unittest
import unittest.mock as mock
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
import models
from models import AuthUserType
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from enum import Enum


KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_SID = 'request_sid'
KEY_DATA = 'data'
KEY_MESSAGE = 'message'
KEY_EMAIL = 'email'
KEY_USER = 'user'
KEY_PIC = 'pic'


class MockAuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"

class MockedAuthUser:
  
    auth_type = ''
    username = ''
    email = ''
    picUrl = ''
    
    def __init__(self, auth_type, name, email, pic=''):
        assert type(auth_type) is MockAuthUserType
        self.auth_type = auth_type.value
        self.username = name
        self.email = email
        self.picUrl = pic
        
class MockedConnection:
    sid = ''
    user = 1

    def __init__(self, sid, user):
        self.sid = sid
        self.user = user
        
        
class testOnGoogleLogin(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_SID: '123456789ABCDEF',
                    KEY_DATA: 
                        
                        {
                    KEY_USER : 'navado',
                    KEY_EMAIL : 'nrw24@spu.edu',
                    KEY_PIC : 'picture',
                    },
                    
                },
               
                },
        ]
        
    def mocked_user(self):
         return MockedAuthUser( MockAuthUserType.GOOGLE, 'testUser', 'testEmail', pic='')
         
    def mocked_connection(self):
        return MockedConnection('123456789ABCDEF', 1)
        
    @mock.patch('app.flask')
    def test_google_login_success(self, mock_flask):
            session = UnifiedAlchemyMagicMock()
            for test in self.success_test_params:
                mock_flask.request.sid = test[KEY_INPUT][KEY_SID]
                mocked_connection = mock.MagicMock()
                mocked_connection.user = 1
                mocked_connection.sid = test[KEY_INPUT][KEY_SID]
                #app.accept_google_login.connection = mocked_connection
                
                with mock.patch("models.DB.session", session):
                    session.add(models.CurrentConnections(mock_flask.request.sid, 1))
                    session.commit()
                    session.query(models.AuthUser).filter_by.return_value.first.return_value = self.mocked_user()
                    
                    session.query(models.CurrentConnections).filter_by.return_value.first.return_value = self.mocked_connection()
                    print("Mocked Login")
                    
                    app.accept_google_login(test[KEY_INPUT][KEY_DATA])
            
              
if __name__ == "__main__":
    unittest.main()