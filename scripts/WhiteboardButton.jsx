import * as React from 'react';
import Whiteboard from './Whiteboard'

function WhiteboardButton() {
  const [display, setDisplay] = React.useState(false);
  
  function switchDisplay(){
      setDisplay(!display)
  }
  
  return (
    <div id="whiteboard componant">
      <button type="button" onClick={switchDisplay}> Whiteboard </button>
     {
       display
       ? <Whiteboard />
       : <div />
     }
    </div>
  );
}

export default WhiteboardButton;