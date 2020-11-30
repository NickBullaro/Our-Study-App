import * as React from 'react';
import Socket from './Socket';

function JoinedRoomsList() {
  const [roomsList, setRoomslist] = React.useState([]);

  function setup() {
    React.useEffect(() => {
      Socket.on('updated room list', (data) => {
        console.log('recieved updated joined room list');
        setRoomslist(data.rooms);
      });
    });
  }

  function enterRoom(roomId) {
    console.log('Sending request to enter room identified by %s', roomId);
    Socket.emit('room entry request', {
      roomId,
    });
  }

  setup();

  return (
      <div id="roomlist_container">
     <div id="joinedRoomList">
       {roomsList.map((room, index) => (
         <div key={index} className="RoomListElement">
           <p className="RoomListName">{room.roomName}</p>
           <button className="RoomListButton" onClick={(event) => enterRoom(room.roomId)} type="submit">Enter room</button>
         </div>
       ))}
     </div>
     </div>
    );
  }

export default JoinedRoomsList;