import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';
import Chatbox from './Chatbox';
import WhiteboardButton from './WhiteboardButton';
import RoomStats from './RoomStats';
import UsersInRoomList from './UsersInRoomList';


function InRoomScreen() {
  
  function tempRoomLeave() {
    Socket.emit('leave room', {
      msg: '',
    });
  }

  return (
    <div id="inRoomScreen">
      <RoomStats />
      <WhiteboardButton />
      <div className="inRoom_chat_usr_container">
        <Chatbox />
        <UsersInRoomList />
      </div>
      <Flashcards />
      <button onClick={tempRoomLeave} type="submit">LeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;
