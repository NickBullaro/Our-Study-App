import * as React from 'react';
import Socket from './Socket';
import VideoRooms from './VideoRooms';

const Stream = () => {
    const [tokens, setToken] = React.useState(null);
    const [roomName, setRoomName] = React.useState('');
    const [username, setUsername] = React.useState('');
    
    const handleLogout = React.useCallback(event => {
        setToken(null);
    }, []);
    
    React.useEffect(event => {
        Socket.on('token', (data) => {
            console.log("ssss");
            if(tokens !== data['tokens'])
            {
                setToken(data['tokens']);
                setRoomName(data['room']);
                setUsername(data['username']);
                console.log("set a token", data['tokens']);
                console.log("set a roomID", data['room']);
                console.log("set a username", data['username']);
            }
        });
    }, [username, roomName]);




    return(
        <div>
        {tokens ? (
            <VideoRooms token={tokens} roomName={roomName}/>
            ) : (
                '')}
        </div>
    );
};

export default Stream;