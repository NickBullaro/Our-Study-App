import * as React from 'react';
import Twilio from 'twilio-video';
import Participant from './VideoParticipants';

const Video = ({token, roomName, username}) => {
  const [room, setRoom] = React.useState(null);
  const [participants, setParticipants] = React.useState([]);
  const [usernamee, setUsername] = React.useState('');
  const [status, setStatus] = React.useState(false);
  const [videoDevice, setVideoDevice] = React.useState([]);
  const [audioDevice, setAudioDevice] = React.useState([]);
  
  if(usernamee !== username)
  {
    setUsername(username);
  }
  
  function changeStatus () {
    setStatus(true);
  }
  
  React.useEffect(() => {
    window.navigator.mediaDevices.enumerateDevices()
      .then(function(devices)
      {
        devices.forEach(function(device)
        {
          if(device.kind == 'videoinput')
          {
            setVideoDevice(device.kind);
          }
          if(device.kind == 'audioinput')
          {
            setAudioDevice(device.kind);
          }
        });
        return changeStatus();
      });
    }, []);
  
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
    if(status == true)
    {
      if(videoDevice == 'videoinput' && audioDevice == 'audioinput')
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
      else if(videoDevice != 'videoinput' && audioDevice == 'audioinput')
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
      else
      {
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
            console.log("disconnect");
            currentRoom.disconnect();
            return null;
          } else {
            return currentRoom;
          }
        });
      };
    }
  }, [usernamee, status]);

  const remoteParticipants = participants.map(participant => (
    <Participant key={participant.sid} participant={participant} />
  ));

  return (
    <div className="videoRoom">
      <div>
        {room ? (
          <Participant
            key={room.localParticipant.sid}
            participant={room.localParticipant}
          />
        ) : (
          ''
        )}
      </div>
      <h3>Remote Participants</h3>
      <div>{remoteParticipants}</div>
    </div>
  );
};

export default Video;