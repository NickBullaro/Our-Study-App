import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';
import Chatbox from './Chatbox';
import WhiteboardButton from './WhiteboardButton';
import RoomStats from './RoomStats';
import UsersInRoomList from './UsersInRoomList';
import FlashcardTest from './FlashcardTest';
import Stream from './Stream';

function InRoomScreen() {
  function tempRoomLeave() {
    Socket.emit('leave room');
  }

  function roomSettings() {

  }

  function logout() {

  }

  function Refresh() {
    Socket.emit('resend in room data');
  }

  return (
    <div id="inRoomScreen">
      <RoomStats />
      <div id="grid_container">
        <div className="container" id="chat_and_users"style={{background:"none"}}>
          <Chatbox />
          <div className="container" id="flashcards_container">
            <Flashcards />
          </div>
      </div>
      <WhiteboardButton />
      <Stream />
      <div className="button_area" id="inRoomScreen">
        <button id="leave_room" onClick={tempRoomLeave} type="submit">Leave Room</button>
        <button id="room_settings" onClick={roomSettings} type="submit">Settings</button>
        <button id="logout" onClick={logout} type="submit">Log Out</button>
      </div>
      <p id="about_link"><a href="about.html"> About Our Study </a></p>
      <button id="refresh_button" onClick={Refresh} type="submit"><img src="/static/refresh_icon.jpg" id="refresh_image" /></button>
    </div>
    </div>
  );
}

export default InRoomScreen;
