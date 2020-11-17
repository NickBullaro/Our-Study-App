import * as React from 'react';
import Socket from './Socket';


function RoomStats() {
  const [roomId, setRoomId] = React.useState('-1');
  const [roomPassword, setRoomPassword] = React.useState('AAAA');
  
  function setup() {
    React.useEffect(() => {
      Socket.on('room stats emitted', (data) => {
        setRoomId(data.roomId);
        setRoomPassword(data.roomPassword);
      })
    });
      
  }
  
  setup();

  return (
    <div id="roomStats">
      <p>Room Id: { roomId }</p>
      <p>Room Password: { roomPassword }</p>
    </div>
  );
}

export default RoomStats;
