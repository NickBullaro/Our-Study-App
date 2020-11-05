import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';

function InRoomScreen() {
  
  function fakeRoomLeave() {
    Socket.emit('leave room', {
      msg: ""
    });
  }

  return (
    <div id='inRoomScreen'>
        <p>Insert room HTML and components here</p>
        <Flashcards />
        <button onClick={ fakeRoomLeave }>FakeLeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;