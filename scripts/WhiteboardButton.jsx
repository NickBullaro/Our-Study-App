import * as React from 'react';
import Whiteboard from './Whiteboard';
import Socket from './Socket';

function WhiteboardButton() {
  const [display, setDisplay] = React.useState(false);
  const [picked, setPicked] = React.useState(false);
  const [whiteboards, setWhiteboards] = React.useState([]);
  const [newName, setNewName] = React.useState("");
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
    setPicked(true);
    Socket.emit("join whiteboard", whiteboards[itx])
  }
  function handleName(event){
    setNewName(event.target.value);
  }
  
  function createBoard(){
    Socket.emit("make whiteboard", {name:newName})
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
        return (<Whiteboard />)
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
          <input id="new" name="new" type="text" onChange={(e) => handleName(e)}/>
        </label>
        <button type="button" onClick={createBoard}>Create</button>
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
