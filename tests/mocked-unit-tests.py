import unittest
import unittest.mock as mock
import os, sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_RESPONSE = 'response'

KEY_ANSWER = 'answer'
KEY_QUESTION = 'question'
KEY_ROOM = 'room'
KEY_DATA = 'data'

KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_SID = 'request_sid'
KEY_NUM_ADDITIONS =  'times_in_database'

KEY_EMIT_ID = 'emit_id'
KEY_EMIT_ROOM = 'room'

class testOnNewCards(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_SID: '123456789ABCDEF',
                    KEY_DATA: 
                        [
                        {
                    KEY_QUESTION: '2+2',
                    KEY_ANSWER : 4,
                    KEY_ROOM: 2
                    },
                    ]
                },
                KEY_EXPECTED: ('2+2', 4, '123456789ABCDEF') 
                },
        ]
        self.failure_test_params = [
           {
                KEY_INPUT: 
                    {
                    KEY_QUESTION: '2+2',
                    KEY_ANSWER : '4',
                    KEY_ROOM : 1
                    },
                
                KEY_EXPECTED: ['<card> question: 2+2 answer: 4 room: 123456789ABCDEF</card>']
            },
            ]
            
    @mock.patch('app.flask')
    def test_new_cards_success(self, mock_flash):
            session = UnifiedAlchemyMagicMock()
            for test in self.success_test_params:
                mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
                app.new_cards.room = test[KEY_INPUT][KEY_DATA][0][KEY_ROOM]
                with mock.patch("models.DB.session", session):
                    app.new_cards(test[KEY_INPUT][KEY_DATA])
            
                query = session.query(models.Flashcards).all()[0]
                expected = test[KEY_EXPECTED]
                print(query.room)
                self.assertEqual(query.room, expected[2])
                self.assertEqual(query.answer, expected[1])  
                self.assertEqual(query.question, expected[0])  

class testEmitFlashCards(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_EMIT_ID: 'cards',
                    KEY_DATA: [{'question' : 'question', 'answer': 'answer'}],
                    KEY_SID: '123456789ABCDEF'
                    },
                KEY_EXPECTED: ('2+2', 4, '123456789ABCDEF') 
                },
        ]
 
        self.hold = ''
            
     def mock_emit(self, sid, data, room='default'):
        self.hold - {KEY_EMIT_ID: sid, KEY_DATA: data, KEY_EMIT_ROOM: room}
        
     @mock.patch('app.flask')
     def test_emit_cards_success(self, mock_flash):
        session = UnifiedAlchemyMagicMock()
        for test in self.success_test_params:
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    app.emit_flashcards(test[KEY_INPUT][KEY_DATA])
        
               

    
if __name__ == "__main__":
    unittest.main()