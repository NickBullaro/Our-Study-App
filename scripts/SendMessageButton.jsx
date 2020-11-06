import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    
    Socket.emit('new message input', {
        'message': newMessage.value
    })
    console.log('Sent the message ' + newMessage.value + ' to server!');
    newMessage.value = '';
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit} className="submitButton">
            <input id="message_input" placeholder="Enter a message" className="input" autoComplete="off"></input>
            <button className="addButton">Chat!</button>
        </form>
    );
}