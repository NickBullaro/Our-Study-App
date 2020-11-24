import * as React from 'react';
import InRoomScreen from './InRoomScreen';
import RoomSelectionScreen from './RoomSelectionScreen';
import Socket from './Socket';

function LoggedInContent() {
  const [joinedRoom, setRoomParticipation] = React.useState(false);
  const [kickedAlready, setKickedAlready] = React.useState(false);
      
  function sendLeaveRoom(roomId) {
    if (!kickedAlready) {
      setKickedAlready(true);
      Socket.emit('i was kicked', {
        roomId: roomId
      });
    }
  }
  
  function leaveRoom() {
    setRoomParticipation(false);
    setKickedAlready(true);
  }
  
  function setup() {
    React.useEffect(() => {
      Socket.on('room entry accepted', () => {
        setRoomParticipation(true);
      });
    });

    React.useEffect(() => {
      Socket.on('left room', () => {
        leaveRoom();
      });
    });
    
    React.useEffect(() => {
      Socket.on('kicked', (data) => {
        sendLeaveRoom(data.roomId);
      });
    });
  }

  setup();

  return (
    <div id="loggedInContent">
      {
        joinedRoom
          ? <InRoomScreen />
          : <RoomSelectionScreen />
      }
    </div>
  );
}

export default LoggedInContent;
