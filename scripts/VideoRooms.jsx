import * as React from 'react';
import Twilio from 'twilio-video';
import Participant from './VideoParticipants';

const Video = ({token, roomName, handleLogout}) => {
  const [room, setRoom] = React.useState(null);
  const [participants, setParticipants] = React.useState([]);

  React.useEffect(() => {
    const participantConnected = participant => {
      console.log('Participant', participant.identity, 'connected.');
      setParticipants(prevParticipants => [...prevParticipants, participant]);
    };

    const participantDisconnected = participant => {
      console.log('Participant', participant.identity, 'disconnected.');
      setParticipants(prevParticipants =>
        prevParticipants.filter(p => p !== participant)
      );
    };
    const videoDevices = [];
    const audioDevices = [];
    window.navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {
      devices.forEach(function(device) {
        if(device.kind == 'videoinput')
        {
          videoDevices.push(device.kind);
        }
        if(device.kind == 'audioinput')
        {
          audioDevices.push(device.kind);
        }
      });
    });
    if(videoDevices[0] == 'videoinput' && audioDevices[0] == 'audioinput')
    {
      Twilio.connect(String(token), {name: roomName}).then(room => {
        setRoom(room);
        room.on('participantConnected', participantConnected);
        room.on('participantDisconnected', participantDisconnected);
        room.participants.forEach(participantConnected);
      }).catch((error) => {
        console.log(error);
      });
    }
    else if(videoDevices[0] != 'videoinput' && audioDevices[0] == 'audioinput')
    {
      Twilio.connect(String(token), {name: roomName, video: false, audio: true}).then(room => {
        setRoom(room);
        room.on('participantConnected', participantConnected);
        room.on('participantDisconnected', participantDisconnected);
        room.participants.forEach(participantConnected);
      }).catch((error) => {
        console.log(error);
      });
    }
    else{
      Twilio.connect(String(token), {name: roomName, video: false, audio: false}).then(room => {
        setRoom(room);
        room.on('participantConnected', participantConnected);
        room.on('participantDisconnected', participantDisconnected);
        room.participants.forEach(participantConnected);
      }).catch((error) => {
        console.log(error);
      });
    }

    return () => {
      setRoom(currentRoom => {
        if (currentRoom && currentRoom.localParticipant.state === 'connected') {
          currentRoom.localParticipant.tracks.forEach(function(trackPublication) {
            trackPublication.track.stop();
          });
          currentRoom.disconnect();
          console.log("$", participants);
          return null;
        } else {
          return currentRoom;
        }
      });
    };
  }, [roomName]);

  const remoteParticipants = participants.map(participant => (
    <Participant key={participant.sid} participant={participant} />
  ));

  return (
    <div className="videoRoom">
      <div className="local-participant">
        {room ? (
          <Participant
            key={room.localParticipant.sid}
            participant={room.localParticipant}
          />
        ) : (
          'hi'
        )}
      </div>
      <div>
        <ul>
          {
            participants.map((participant, index) => <li key={index}>{participant.identity}</li>)
          }
        </ul>
      </div>
      <h3>Remote Participants</h3>
      <div className="remote-participants">{remoteParticipants}</div>
    </div>
  );
};

export default Video;