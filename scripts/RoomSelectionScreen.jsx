import * as React from 'react';
import Socket from './Socket';

function RoomSelectionScreen() {
  
  function fakeRoomEnter() {
    Socket.emit('room entry request', {
      msg: ""
    });
  }

  return (
    <div id='roomSelectionScreen'>
        <p>Insert Room Selection Screen HTML and components here</p>
        <button onClick={ fakeRoomEnter }>FakeEnterRoom</button>
    </div>
  );
}

export default RoomSelectionScreen;