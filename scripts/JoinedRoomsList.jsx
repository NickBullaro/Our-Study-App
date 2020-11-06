import * as React from 'react';
import * as ReactDOM from 'react-dom';
import Socket from './Socket';
import InRoomScreen from './InRoomScreen';

function JoinedRoomsList() {
  const [roomsList, setRoomslist] = React.useState([]);

  function setup() {
    React.useEffect(() => {
      Socket.on('updated room list', (data) => {
        console.log("recieved updated joined room list")
        setRoomslist(data.rooms)
      });
    });
  }
  
  function enterRoom(roomId) {
    console.log("Sending request to enter room identified by %i", roomId)
    Socket.emit('room entry request', {
      roomId: roomId
    });
  }
  
  setup();

  return (
    <div id='joinedRoomList'>
      <ul>
        {roomsList.map((room, index) => 
          <li key={index} className='RoomListElement'>
            <p className='RoomListName'>{room.roomName}</p>
            <button className='RoomListButton' onClick={(event) => enterRoom(room.roomId)} type='submit'>Enter room</button>
          </li>)}
      </ul>
    </div>
  );
}

export default JoinedRoomsList;
