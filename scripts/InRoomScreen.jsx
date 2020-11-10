import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';
import Chatbox from './Chatbox';
import WhiteboardButton from './WhiteboardButton'

function InRoomScreen() {
  function fakeRoomLeave() {
    Socket.emit('leave room', {
      msg: '',
    });
  }

  return (
    <div id="inRoomScreen">
      <p>Insert room HTML and components here</p>
      <WhiteboardButton />
      <p>Chatbox</p>
      <Chatbox />
      <Flashcards />
      <button onClick={fakeRoomLeave} type="submit">FakeLeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;
