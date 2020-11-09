import * as React from 'react';

function Whiteboard() {
  const [marks, setMarks] = React.useState([])
  const canvasRef = React.useRef(null)
  
  React.useEffect(() => {
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    //Our first draw
    context.fillStyle = '#00ff00'
    context.fillRect(0, 0, context.canvas.width, context.canvas.height)
  }, [])
  return (
    <canvas ref={canvasRef}/>
  );
}

export default Whiteboard;