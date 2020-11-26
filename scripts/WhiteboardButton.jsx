import * as React from 'react';
import Whiteboard from './Whiteboard';
import Socket from './Socket';

function WhiteboardButton() {
  const [display, setDisplay] = React.useState(false);
  const [picked, setPicked] = React.useState(false);
  const [whiteboards, setWhiteboards] = React.useState([]);
  const [boardPicked, setBoardPicked] = React.useState(0)
  
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
  
  function fGotWhiteboards(data) {
    setWhiteboards(data);
  }
  function newGotWhiteboards() {
    Socket.on('got whiteboard', fGotWhiteboards);
    return () => Socket.off('got whiteboard', fGotWhiteboards);
  }
  React.useEffect(newGotWhiteboards);

  

  return (
    <div id="whiteboard_component">
      <button type="button" onClick={switchDisplay}>Whiteboard</button>
      {{
        if(display)
        {
          if(picked)
          {
            <Whiteboard board={boardPicked}/>
          }
          else
          {
            <form>
              <label>New Board:
                <input id="new" name="new" type="text" />
              </label>
              <input type="submit" id="new" name="new" value="Create" />
            </form>
          }
        }
     }}
    </div>
  );
}

export default WhiteboardButton;
