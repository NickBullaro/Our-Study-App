import * as React from 'react';
import SendMessageButton from './SendMessageButton';
import Socket from './Socket';

function Chatbox() {
  const [messages, setMessages] = React.useState([]);

  function updateMessages(data) {
    setMessages(data.allMessages);
    const chatBox = document.getElementById('chatbox');
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function getNewMessage() {
    React.useEffect(() => {
      Socket.on('sending room data', updateMessages);
      return () => {
        Socket.off('sending room data', updateMessages);
      };
    });
  }

  getNewMessage();

  return (
    <div>
      <h3>HI</h3>
      <div className="userList">
        <h1>Messages!</h1>
        <ul id="chatbox">
          {
            messages.map((message, index) => <li key={index}>{message}</li>)
          }
        </ul>
      </div>
      <SendMessageButton />
    </div>
  );
}

export default Chatbox;
