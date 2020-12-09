import * as React from 'react';
import Socket from './Socket';

function RoomJoinCreate() {
  const [createRoom, setCreateRoom] = React.useState(true);

  function switchToCreate() {
    setCreateRoom(true);
  }

  function switchToJoin() {
    setCreateRoom(false);
  }

  function createNewRoom(event) {
    const newRoom = document.getElementById('create_input');
    Socket.emit('new room creation request', {
      roomName: newRoom.value,
    });

    newRoom.value = '';

    event.preventDefault();
  }

  function joinExistingRoom(event) {
    const roomId = document.getElementById('join_room_id_input');
    const roomPassword = document.getElementById('join_room_password_input');
    Socket.emit('join room request', {
      roomId: roomId.value,
      roomPassword: roomPassword.value,
    });

    roomId.value = '';
    roomPassword.value = '';

    event.preventDefault();
  }

  return (
    <div className="container" id="roomJoinCreateButtons">
      <div id="roomJCB_message">Not what you are looking for?</div>
      {
          createRoom
            ? (
              <div id="JCB_container">
                <div id="main_buttons_container">
                  <button id="start_create_active" onClick={switchToCreate} type="submit">Create Room</button>
                  <button id="start_join" onClick={switchToJoin} type="submit">Join Room</button>
                </div>
                <form onSubmit={createNewRoom} id="createRoomForm" style={{ borderTopRightRadius: '10px' }}>
                  <div id="input_desc">Enter room name:</div>
                  <input id="create_input" placeholder="room name" />
                  <button id="create_room_button" type="submit">Create</button>
                </form>
              </div>
            )
            : (
              <div id="JCB_container">
                <div id="main_buttons_container">
                  <button id="start_create" onClick={switchToCreate} type="submit">Create Room</button>
                  <button id="start_join_active" onClick={switchToJoin} type="submit">Join Room</button>
                </div>
                <form onSubmit={joinExistingRoom} id="joinRoomForm" style={{ borderTopLeftRadius: '10px' }}>
                  <div id="input_desc">Enter room id:</div>
                  <input id="join_room_id_input" placeholder="room id" />
                  <div id="input_desc">Enter password:</div>
                  <input id="join_room_password_input" placeholder="password" />
                  <button id="join_room_button" type="submit">Join</button>
                </form>
              </div>
            )
        }
    </div>
  );
}

export default RoomJoinCreate;
