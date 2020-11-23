import * as React from 'react';
import JoinedRoomsList from './JoinedRoomsList';
import RoomJoinCreate from './RoomJoinCreate';

function RoomSelectionScreen() {
  return (
    <div id="roomSelectionScreen">
    <h2 className="header">Existing Rooms</h2>
      <JoinedRoomsList />
      <RoomJoinCreate />
    </div>
  );
}

export default RoomSelectionScreen;
