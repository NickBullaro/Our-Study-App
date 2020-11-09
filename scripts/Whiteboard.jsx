import * as React from 'react';

function Whiteboard() {
  const [isDrawing, setIsDrawing] = React.useState(()=>[false]);
  const [doDraw, setDoDraw] = React.useState([]);
  const canvasRef = React.useRef(null);
  const [oldCoor, setOldCoor] = React.useState(()=>{return {y:0,x:0}});
  const [newCoor, setNewCoor] = React.useState(()=>{return {y:0,x:0}});
  const [listersOff, setListersOff] = React.useState(true);
  
  function startDraw(cursor){
    console.log("cursor down")
    isDrawing[0]=true;
    setIsDrawing(isDrawing);
    oldCoor.y=cursor.offsetY;
    oldCoor.x=cursor.offsetX;
    newCoor.y=cursor.offsetY;
    newCoor.x=cursor.offsetX;
    setOldCoor(oldCoor);
    setNewCoor(newCoor);
  }
  function draw(cursor){
    if (isDrawing[0]){
      console.log(oldCoor.x, oldCoor.y,newCoor.x, newCoor.y)
      oldCoor.y=newCoor.y;
      oldCoor.x=newCoor.x;
      setNewCoor((myDict)=>{
        myDict.x=cursor.offsetX;
        myDict.y=cursor.offsetY;
        return myDict
      })
      setOldCoor(oldCoor);
      setDoDraw([])
    }
  }
  function endDraw(cursor){
    isDrawing[0]=false;
    setIsDrawing(isDrawing);
    oldCoor.y=newCoor.y;
    oldCoor.x=newCoor.x;
    setNewCoor({y:cursor.offsetY,x:cursor.offsetX});
    setOldCoor(oldCoor);
  }
  
  React.useEffect(() => {
    const canvas = canvasRef.current
    if(listersOff){
      canvas.addEventListener('mousedown', startDraw, false);
      canvas.addEventListener('mousemove', draw, false);
      canvas.addEventListener('mouseup', endDraw, false);
      setListersOff(false)
    }
    const context = canvas.getContext('2d')
    context.fillStyle = '#000000'
    //Our first draw
    console.log("HELLO")
    context.moveTo(oldCoor.x, oldCoor.y);
    context.lineTo(newCoor.x, newCoor.y);
    context.stroke();
  }, [doDraw])
  return (
    <canvas ref={canvasRef}/>
  );
}

export default Whiteboard;