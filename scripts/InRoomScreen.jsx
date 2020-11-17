import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';
import Chatbox from './Chatbox';
import WhiteboardButton from './WhiteboardButton';

function InRoomScreen() {
  const [users, setUsers] = React.useState([]);
  const [picUrls, setUrls] = React.useState([]);
  
  function fakeRoomLeave() {
    Socket.emit('leave room', {
      msg: '',
    });
  }

  function updateUsers(data) {
    console.log(`Received new user: ${data.all_users}`);
    setUsers(data.all_users);
    setUrls(data.all_user_pics);
  }

  function getNewUser() {
    React.useEffect(() => {
      Socket.on('users received', (data) => {
        setUsers(data.all_users);
        setUrls(data.all_user_pics);
      })
    });
  }

  getNewUser();

  return (
    <div id="inRoomScreen">
      <WhiteboardButton />
      <div className="inRoom_chat_usr_container">
        <Chatbox />
        <ul className="userListing">
          <h1 className="UserTitle"> Users: </h1>
          {
            users.map((user, index) => <li key={index}><img src={picUrls[index]} className="img"></img> {user}</li>)
          }
        </ul>
      </div>
        <div id="flashcards">
          <Flashcards />
        </div>
      <button onClick={fakeRoomLeave} type="submit">FakeLeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;
