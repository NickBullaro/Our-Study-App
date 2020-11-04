import * as React from 'react';
import Socket from './Socket';
import JoinedRoomsList from './JoinedRoomsList';
import RoomJoinCreate from './RoomJoinCreate';

function RoomSelectionScreen() {
  
  function fakeRoomEnter() {
    Socket.emit('room entry request', {
      msg: ""
    });
  }

  return (
    <div id='roomSelectionScreen'>
        <p>Insert Room Selection Screen HTML and components here</p>
        <JoinedRoomsList />
        <RoomJoinCreate />
    </div>
  );
}

export default RoomSelectionScreen;