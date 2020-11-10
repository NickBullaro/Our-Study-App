import * as React from 'react';
import Socket from './Socket'

function Whiteboard() {
  const [isDrawing, setIsDrawing] = React.useState(()=>[false]);
  const [doDraw, setDoDraw] = React.useState({oldx:0,oldy:0,newx:0,newy:0,color:"#000000"});
  const canvasRef = React.useRef(null);
  const [stroke, setStroke] = React.useState(()=>{return {oldx:0,oldy:0,newx:0,newy:0,color:"#000000"}});
  const [listersOff, setListersOff] = React.useState(true);
  
  function startDraw(cursor){
    console.log("cursor down")
    isDrawing[0]=true;
    setIsDrawing(isDrawing);
    stroke.oldy=cursor.offsetY;
    stroke.oldx=cursor.offsetX;
    stroke.newy=cursor.offsetY;
    stroke.newx=cursor.offsetX;
    setStroke(stroke);
  }
  function draw(cursor){
    if (isDrawing[0]){
      stroke.oldy=stroke.newy;
      stroke.oldx=stroke.newx;
      stroke.newy=cursor.offsetY;
      stroke.newx=cursor.offsetX;
      setStroke(stroke);
      Socket.emit("drawing stroke input", stroke);
    }
  }
  function endDraw(cursor){
    isDrawing[0]=false;
    setIsDrawing(isDrawing);
    stroke.oldy=stroke.newy;
    stroke.oldx=stroke.newx;
    stroke.newy=cursor.offsetY;
    stroke.newx=cursor.offsetX;
    setStroke(stroke);
    Socket.emit("drawing stroke input", stroke);
  }
  function changeColor(event){
    stroke.color = event.target.value;
    setStroke(stroke);
  }
  
  function fOutputDoStroke(data) {
    setDoDraw(data);
  }
  function newOutputDoStroke() {
    Socket.on('drawing stroke output', fOutputDoStroke);
    return () => Socket.off('drawing stroke output', fOutputDoStroke);
  }
  React.useEffect(newOutputDoStroke);
  
  React.useEffect(() => {
    const canvas = canvasRef.current
    if(listersOff){
      canvas.addEventListener('mousedown', startDraw, false);
      canvas.addEventListener('mousemove', draw, false);
      canvas.addEventListener('mouseup', endDraw, false);
      canvas.height = 500
      canvas.width = 500
      setListersOff(false)
    }
    const context = canvas.getContext('2d')
    context.beginPath();
    context.strokeStyle = doDraw.color
    context.moveTo(doDraw.oldx, doDraw.oldy);
    context.lineTo(doDraw.newx, doDraw.newy);
    context.stroke();
  }, [doDraw])
  return (
    <div id='whiteboard componant'>
      <canvas ref={canvasRef}/>
      <form onChange={changeColor}>
        <input type="radio" id="black" name="color" value="#000000" />
        <label for="black">Black</label>
        <input type="radio" id="red" name="color" value="#ff0000" />
        <label for="red">Red</label>
        <input type="radio" id="blue" name="color" value="#0000ff"/>
        <label for="blue">Blue</label>
        <input type="radio" id="Green" name="color" value="#00ff00" />
        <label for="green">Green</label>
      </form>
    </div>
  );
}

export default Whiteboard;