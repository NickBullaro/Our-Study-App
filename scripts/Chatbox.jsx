import * as React from 'react';

import { SendMessageButton } from './SendMessageButton';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);

    function getNewMessage() {
        React.useEffect(() => {
            Socket.on('temp', updateMessages);
            return () => {
                Socket.off('temp', updateMessages);
            }
        });
    }

    function updateMessages(data) {
        console.log("Received messages from server: " + data['allMessages']);

        setMessages(data['allMessages']);
        let chatBox = document.getElementById("chatbox");
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    getNewMessage();

    return (
        <div>
            <h3>HI</h3>
            <div className="userList">
                <h1>Messages!</h1>
                    <ul id="chatbox">
                        {
                            messages.map((message, index) => 
                                <li key={index}>{message}</li>)
                        }
                    </ul>
            </div>
            <SendMessageButton />
        </div>
    );
}