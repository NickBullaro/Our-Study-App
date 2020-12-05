import * as React from 'react';
import PropTypes from 'prop-types';
import Socket from './Socket';

function Whiteboard() {
  const [isDrawing, setIsDrawing] = React.useState(() => [false]);
  const [doDraw, setDoDraw] = React.useState({
    oldx: 0, oldy: 0, newx: 0, newy: 0, color: '#000000', size: 1,
  });
  const canvasRef = React.useRef(null);
  const [stroke, setStroke] = React.useState(() => ({
    oldx: 0, oldy: 0, newx: 0, newy: 0, color: '#000000', size: 1,
  }));
  const [listersOff, setListersOff] = React.useState(true);
  const [loading, setLoading] = React.useState(true);

  function ColorPick({ colorName, colorValue }) {
    if (stroke.color === colorValue) {
      return (
        <label htmlFor={colorName}>
          <input type="radio" id={colorName} name="color" value={colorValue} defaultChecked />
          {colorName}
        </label>
      );
    }
    return (
      <label htmlFor={colorName}>
        <input type="radio" id={colorName} name="color" value={colorValue} />
        {colorName}
      </label>
    );
  }
  ColorPick.propTypes = {
    colorName: PropTypes.string.isRequired,
    colorValue: PropTypes.string.isRequired,
  };

  function handleBlob(myBlob) {
    Socket.emit('save', { blob: myBlob });
  }
  function handleSave() {
    const canvas = canvasRef.current;
    canvas.toBlob(handleBlob);
  }
  function handleBlobForce(myBlob) {
    Socket.emit('forced save', { blob: myBlob });
  }
  function startDraw(cursor) {
    isDrawing[0] = true;
    setIsDrawing(isDrawing);
    stroke.oldy = cursor.offsetY;
    stroke.oldx = cursor.offsetX;
    stroke.newy = cursor.offsetY;
    stroke.newx = cursor.offsetX;
    setStroke(stroke);
  }
  function draw(cursor) {
    if (isDrawing[0]) {
      stroke.oldy = stroke.newy;
      stroke.oldx = stroke.newx;
      stroke.newy = cursor.offsetY;
      stroke.newx = cursor.offsetX;
      setStroke(stroke);
      Socket.emit('drawing stroke input', stroke);
    }
  }
  function endDraw(cursor) {
    isDrawing[0] = false;
    setIsDrawing(isDrawing);
    stroke.oldy = stroke.newy;
    stroke.oldx = stroke.newx;
    stroke.newy = cursor.offsetY;
    stroke.newx = cursor.offsetX;
    setStroke(stroke);
    Socket.emit('drawing stroke input', stroke);
  }
  function changeColor(event) {
    stroke.color = event.target.value;
    setStroke(stroke);
  }

  function changeSize(event) {
    stroke.size = event.target.value;
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

  function fLoadBoard(data) {
    if (loading) {
      setLoading(false);
      if ('address' in data) {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const image = new Image(400, 400);
        image.crossOrigin = 'anonymous';
        image.onload = () => {
          context.drawImage(image, 0, 0);
        };
        image.src = data.address;
        console.log(data.address);
      }
    }
  }
  function newLoadBoard() {
    Socket.on('load board', fLoadBoard);
    return () => Socket.off('load board', fLoadBoard);
  }
  React.useEffect(newLoadBoard);

  function fForceToSave() {
    console.log('FORCED SAVE');
    const canvas = canvasRef.current;
    canvas.toBlob(handleBlobForce);
  }
  function newForceToSave() {
    Socket.on('force to save', fForceToSave);
    return () => Socket.off('force to save', fForceToSave);
  }
  React.useEffect(newForceToSave);

  React.useEffect(() => {
    const canvas = canvasRef.current;
    if (listersOff) {
      canvas.addEventListener('mousedown', startDraw, false);
      canvas.addEventListener('mousemove', draw, false);
      canvas.addEventListener('mouseup', endDraw, false);
      canvas.height = 400;
      canvas.width = 400;
      setListersOff(false);
    }
    const context = canvas.getContext('2d');
    context.beginPath();
    if (doDraw.color === '#ff00ff') {
      context.globalCompositeOperation = 'destination-out';
    } else {
      context.globalCompositeOperation = 'source-over';
    }
    context.lineWidth = doDraw.size;
    context.strokeStyle = doDraw.color;
    context.lineCap = 'round';
    context.moveTo(doDraw.oldx, doDraw.oldy);
    context.lineTo(doDraw.newx, doDraw.newy);
    context.stroke();
  }, [doDraw]);
  function Tools() {
    return (
      <div>
        <form onChange={changeColor}>
          <ColorPick colorName="Black" colorValue="#000000" />
          <ColorPick colorName="Blue" colorValue="#0000ff" />
          <ColorPick colorName="Green" colorValue="#00ff00" />
          <ColorPick colorName="Red" colorValue="#ff0000" />
          <ColorPick colorName="Erase" colorValue="#ff00ff" />
        </form>
        <form onChange={changeSize}>
          <label htmlFor="size">
            <input type="number" id="size" name="size" defaultValue={stroke.size} min="1" max="50" />
            Size
          </label>
        </form>
        <button type="button" onClick={handleSave}>Save</button>
      </div>
    );
  }

  return (
    <div id="whiteboard_component" className="container">
      <canvas ref={canvasRef} />
      {
        loading
          ? <h2>LOADING</h2>
          : <Tools />
      }
    </div>
  );
}

export default Whiteboard;
