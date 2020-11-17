import * as React from 'react';
import SendMessageButton from './SendMessageButton';
import Socket from './Socket';

function Chatbox() {
  const [messages, setMessages] = React.useState([]);
  const [picUrls, setUrls] = React.useState([]);

  function getNewMessage() {

    React.useEffect(() => {
      Socket.on('sending message history', (data) => {
        setMessages(data.allMessages);
        setUrls(data.all_user_pics);
        const chatBox = document.getElementById('chatbox');
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    });
  }
  

  getNewMessage();

  return (
    <div>
      <h3>Chatbox</h3>
      <div className="userList"  id="chatbox">
        <ul>
          {
            messages.map((message, index) => <li key={index}><img src={picUrls[index]} className="img"></img> {message}</li>)
          }
        </ul>
      </div>
      <SendMessageButton />
    </div>
  );
}

export default Chatbox;
