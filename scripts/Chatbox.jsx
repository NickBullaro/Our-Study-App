import * as React from 'react';
import SendMessageButton from './SendMessageButton';
import Socket from './Socket';

function Chatbox() {
  const [messages, setMessages] = React.useState([]);
  const [picUrls, setUrls] = React.useState([]);

  function getNewMessage() {
    React.useEffect(() => {
      Socket.on('sending message history',(data) => {
        setMessages(data.allMessages);
        setUrls(data.all_user_pics);
        const chatBox = document.getElementById('chatbox');
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    });
  }

  getNewMessage();

  return (
    <div className="container" id="chatbox">
      <div className="chat_messages">
          {
            messages.map((message, index) => <div className="container" id="registered_message" key={index}><img src={picUrls[index]} className="img"/>{message}</div>)
          }
      </div>
      <SendMessageButton />
    </div>
  );
}

export default Chatbox;
