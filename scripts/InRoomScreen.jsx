import * as React from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';
import Chatbox from './Chatbox';
import WhiteboardButton from './WhiteboardButton';
import RoomStats from './RoomStats';
import UsersInRoomList from './UsersInRoomList';
import FlashcardTest from './FlashcardTest';

function InRoomScreen() {
  const [test, setTest] = React.useState(false);
  const [flashcards, setFlashcards] = React.useState([]);
  function tempRoomLeave() {
    Socket.emit('leave room');
  }
  
  function takeTest(event) {
    event.preventDefault();
    setTest(true);
  }
     const CARDS = 'cards';

  function newCards() {
    React.useEffect(() => {
      Socket.on(CARDS, (data) => {
        setFlashcards(data);
      });
    });
  }

  newCards();
  return (
    test ?
    <FlashcardTest />
    :
    <div id="inRoomScreen">
      <RoomStats />
      <WhiteboardButton />
      <div className="inRoom_chat_usr_container">
        <Chatbox />
        <UsersInRoomList />
      </div>
      <Flashcards flashcards={flashcards} />
      <button onClick={takeTest} value='Take Test' />
      <button onClick={tempRoomLeave} type="submit">LeaveRoom</button>
    </div>
  );
}

export default InRoomScreen;
