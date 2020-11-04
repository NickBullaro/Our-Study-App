import * as React from 'react';
import InRoomScreen from './InRoomScreen';
import RoomSelectionScreen from './RoomSelectionScreen';
import Socket from './Socket';

function LoggedInContent() {
  const [joinedRoom, setRoomParticipation] = React.useState(false);

  function setup() {
    React.useEffect(() => {
      Socket.on('room entry accepted', (data) => {
        setRoomParticipation(true);
      });
    });
    
    React.useEffect(() => {
      Socket.on('left room', (data) => {
        setRoomParticipation(false);
      });
    });
  }
  
  setup();

  return (
    <div id='loggedInContent'>
      {
        joinedRoom?
          <InRoomScreen />
        :
          <RoomSelectionScreen />
      }
    </div>
  );
}

export default LoggedInContent;
