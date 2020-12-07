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
KEY_GET_ROOM_RETURN = 'get_rm_rtn'

KEY_SID = 'request_sid'

KEY_HOLD_LIST = 'emitted'
KEY_HOLD_TYPE = 'captured_emit_type'
KEY_DATA = 'data'
KEY_HOLD_EMIT_FLASHCARDS =  'emit_flashcards'
KEY_HOLD_EMIT_MESSAGES = 'emit_messages'

class testEmitRoomHistory(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT:
                    {
                        KEY_SID: '123456789ABCDEF',
                        KEY_GET_ROOM_RETURN: '123456789ABCDEF'
                    },
                KEY_EXPECTED:
                    {
                        KEY_HOLD_LIST:
                            [{
                                KEY_HOLD_TYPE: KEY_HOLD_EMIT_FLASHCARDS,
                                KEY_DATA: '123456789ABCDEF'
                            },{
                                KEY_HOLD_TYPE: KEY_HOLD_EMIT_MESSAGES,
                                KEY_DATA: '123456789ABCDEF'
                            }]
                    }
            }
            ]
        self.hold = []

     def mock_emit_flashcards(self, room):
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_EMIT_FLASHCARDS, KEY_DATA: room})

     def mock_emit_all_messages(self, client_sid):
        self.hold.append({KEY_HOLD_TYPE: KEY_HOLD_EMIT_MESSAGES, KEY_DATA: client_sid})

     @mock.patch('app.get_room')
     def test_emit_room_history(self, mock_get_room):
        for test in self.success_test_params:
            self.hold = []
            mock_get_room.return_value = test[KEY_INPUT][KEY_GET_ROOM_RETURN]

            with mock.patch("app.emit_all_messages", self.mock_emit_all_messages):
                with mock.patch("app.emit_flashcards", self.mock_emit_flashcards):
                    app.emit_room_history(test[KEY_INPUT][KEY_SID])

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