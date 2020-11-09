import * as React from 'react';
import InRoomScreen from './InRoomScreen';
import RoomSelectionScreen from './RoomSelectionScreen';
import Socket from './Socket';

function LoggedInContent() {
  const [joinedRoom, setRoomParticipation] = React.useState(false);

  function setup() {
    React.useEffect(() => {
      Socket.on('room entry accepted', () => {
        setRoomParticipation(true);
      });
    });

    React.useEffect(() => {
      Socket.on('left room', () => {
        setRoomParticipation(false);
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
