import * as React from 'react';
import Socket from './Socket';
import JoinedRoomsList from './JoinedRoomsList';
import RoomJoinCreate from './RoomJoinCreate';

function RoomSelectionScreen() {
  function Refresh() {
    Socket.emit("resend room selection data");
  }
  
  return (
    <div id="roomSelectionScreen">
      <p id="about_link"><a href="about.html"> About Our Study </a></p>
      <button id="refresh_button" onClick={Refresh} type="submit"><img src="/static/refresh_icon.jpg" id="refresh_image"/></button>
      <h2 className="header">Existing Rooms</h2>
      <JoinedRoomsList />
      <RoomJoinCreate />
    </div>
  );
}

export default RoomSelectionScreen;
