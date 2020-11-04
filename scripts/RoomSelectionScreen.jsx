import * as React from 'react';
import Socket from './Socket';
import JoinedRoomsList from './JoinedRoomsList';
import RoomJoinCreate from './RoomJoinCreate';

function RoomSelectionScreen() {

  return (
    <div id='roomSelectionScreen'>
        <JoinedRoomsList />
        <RoomJoinCreate />
    </div>
  );
}

export default RoomSelectionScreen;