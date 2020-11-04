import * as React from 'react';
import Socket from './Socket';

function InRoomScreen() {
  
  function fakeRoomLeave() {
    Socket.emit('leave room', {
      msg: ""
    });
  }

  return (
    <div id='inRoomScreen'>
        <p>Insert room HTML and components here</p>
        <button onClick={ fakeRoomLeave }>FakeLeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;