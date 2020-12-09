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
      <h2 className="header">Existing Rooms</h2>
      <button id="refresh_button" onClick={Refresh} type="submit">
        <img id="refresh_image" alt="" src="../static/refresh_icon.jpg"/>
      </button>
      <form action="about.html" id="help">
        <button type="submit">?</button>
      </form>
      <div id="about_help">About us</div>
      <JoinedRoomsList />
      <RoomJoinCreate />
    </div>
  );
}

export default RoomSelectionScreen;
