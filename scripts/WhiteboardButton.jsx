import * as React from 'react';
import Whiteboard from './Whiteboard';
import Socket from './Socket';
import NameForm from './NameForm';

function WhiteboardButton() {
  const [display, setDisplay] = React.useState(false);
  const [picked, setPicked] = React.useState(false);
  const [whiteboards, setWhiteboards] = React.useState([]);
  const input = React.useRef(null);

  function switchDisplay() {
    if (!display) {
      Socket.emit('get whiteboards');
    } else {
      Socket.emit('disconnect whiteboard');
      setPicked(false);
    }
    setDisplay(!display);
  }
  function handleRemove(itx) {
    Socket.emit('remove whiteboard', whiteboards[itx]);
  }

  function handleJoin(itx) {
    setPicked(true);
    Socket.emit('join whiteboard', whiteboards[itx]);
  }

  function createBoard() {
    Socket.emit('make whiteboard', { name: input.current.value });
    console.log(input.current.value);
  }

  function fGotWhiteboards(data) {
    setWhiteboards(data);
  }
  function newGotWhiteboards() {
    Socket.on('got whiteboard', fGotWhiteboards);
    return () => Socket.off('got whiteboard', fGotWhiteboards);
  }
  React.useEffect(newGotWhiteboards);

  function Picking() {
    if (picked) {
      return (<Whiteboard />);
    }
    return (
      <div>
        {whiteboards.map((field, idx) => (
          <div key={`${field.name + idx}`}>
            <button type="button" onClick={() => handleJoin(idx)}>{field.name}</button>
            <button type="button" onClick={() => handleRemove(idx)}>X</button>
          </div>
        ))}
        <NameForm myRef={input} />
        <button type="button" onClick={createBoard}>Create</button>
      </div>
    );
  }

  return (
    <div id="whiteboard_component">
      <button type="button" onClick={switchDisplay}>Whiteboard</button>
      {
       display
         ? <Picking />
         : <div />
     }
    </div>
  );
}

export default WhiteboardButton;
