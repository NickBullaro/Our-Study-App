import * as React from 'react';

const Participant = ({ participant }) => {
    const [videoTracks, setVideoTracks] = React.useState([]);
    const [audioTracks, setAudioTracks] = React.useState([]);
    
    const videoRef = React.useRef();
    const audioRef = React.useRef();
    
    const trackpubsToTracks = trackMap => Array.from(trackMap.values())
      .map(publication => publication.track)
      .filter(track => track !== null);
    
    
    React.useEffect(() => {
      const trackSubscribed = track => {
        if (track.kind === 'video') {
          setVideoTracks(videoTracks => [...videoTracks, track]);
        } else {
          console.log("audio");
          setAudioTracks(audioTracks => [...audioTracks, track]);
        }
      };
    
      const trackUnsubscribed = track => {
        if (track.kind === 'video') {
          setVideoTracks(videoTracks => videoTracks.filter(v => v !== track));
        } else {
          setAudioTracks(audioTracks => audioTracks.filter(a => a !== track));
        }
      };
      
      setVideoTracks(trackpubsToTracks(participant.videoTracks));
      setAudioTracks(trackpubsToTracks(participant.audioTracks));
  
      participant.on('trackSubscribed', trackSubscribed);
      participant.on('trackUnsubscribed', trackUnsubscribed);
  
      return () => {
        setVideoTracks([]);
        setAudioTracks([]);
        participant.removeAllListeners();
      };
    }, [participant]);
  
    React.useEffect(() => {
        const videoTrack = videoTracks[0];
        if (videoTrack) {
          videoTrack.attach(videoRef.current);
          return () => {
            videoTrack.detach();
          };
        }
    }, [videoTracks]);
    
    
    React.useEffect(() => {
        const audioTrack = audioTracks[0];
        if (audioTrack) {
          console.log("audioAttach", participant);
          audioTrack.attach(audioRef.current);
          return () => {
            console.log("audioDetach");
            audioTrack.detach();
          };
        }
    }, [audioTracks]);
  
  
    return (
        <div>
            <h3>{participant.identity.toString()}</h3>
            { videoTracks[0] ? (
                <video ref={videoRef} autoPlay={true}></video>
                ) : (
                <img className ='noCamera' src='../static/482929.svg'></img>)
            }
            <audio ref={audioRef} autoPlay={true}></audio>
        </div>
    );
//}
};

export default Participant;