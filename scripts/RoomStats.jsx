import * as React from 'react';
import Socket from './Socket';

function RoomStats() {
  const [roomId, setRoomId] = React.useState('-1');
  const [roomPassword, setRoomPassword] = React.useState('AAAA');
  const [roomName, setRoomName] = React.useState('Room Name');

  function setup() {
    React.useEffect(() => {
      Socket.on('room stats update', (data) => {
        setRoomId(data.roomId);
        setRoomPassword(data.roomPassword);
        setRoomName(data.roomName);
      });
    });
  }

  function resetPassword() {
    Socket.emit('reset password');
  }

  setup();

  return (
    <div id="roomStats">
      <h2 className="header">{ roomName }</h2>
      <p>
        Room Id:
        { roomId }
        {' '}
        Room Password:
        { roomPassword }
      </p>
      <button onClick={resetPassword} type="submit">ResetPassword</button>
    </div>
  );
}

export default RoomStats;
