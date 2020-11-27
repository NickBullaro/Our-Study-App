import * as React from 'react';
import Whiteboard from './Whiteboard';
import Socket from './Socket';

function WhiteboardButton() {
  const [display, setDisplay] = React.useState(false);
  const [picked, setPicked] = React.useState(false);
  const [whiteboards, setWhiteboards] = React.useState([]);
  const [boardPicked, setBoardPicked] = React.useState(false);
  const [boardID, setBoardID] = React.useState("");
  function switchDisplay() {
    if(display)
    {
      Socket.emit("get whiteboards");
    }
    else
    {
      setPicked(false)
    }
    setDisplay(!display);
  }
  function handleRemove(itx) {
    Socket.emit("remove whiteboard", whiteboards[itx])
  }
  
  function handleJoin(itx) {
    setBoardPicked(true);
    setBoardID(whiteboards[itx].id);
  }
  
  function fGotWhiteboards(data) {
    setWhiteboards(data);
  }
  function newGotWhiteboards() {
    Socket.on('got whiteboard', fGotWhiteboards);
    return () => Socket.off('got whiteboard', fGotWhiteboards);
  }
  React.useEffect(newGotWhiteboards);
  
  function Picking(){
      if(picked)
      {
        return (<Whiteboard board={boardPicked}/>)
      }
      return(
        <div>
          {whiteboards.map((field, idx) => (
            <div key={`${field.name + idx}`}>
              <button type="button" onClick={() => handleJoin(idx)}>{field.name}</button>
              <button type="button" onClick={() => handleRemove(idx)}>X</button>
            </div>
          ))}
        <label>New Board:
          <input id="new" name="new" type="text" />
        </label>
        <input type="submit" id="new" name="new" value="Create" />
      </div>
      )
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
