import * as React from 'react';
import Socket from './Socket';


function RoomStats() {
  const [roomId, setRoomId] = React.useState('-1');
  const [roomPassword, setRoomPassword] = React.useState('AAAA');
  
  function setup() {
    React.useEffect(() => {
      Socket.on('room stats update', (data) => {
        setRoomId(data.roomId);
        setRoomPassword(data.roomPassword);
      })
    });
      
  }
  
  function resetPassword () {
    Socket.emit('reset password');
  }
  
  setup();

  return (
    <div id="roomStats">
      <p>Room Id: { roomId }</p>
      <p>Room Password: { roomPassword }</p>
      <button onClick={resetPassword} type="submit">ResetPassword</button>
    </div>
  );
}

export default RoomStats;
