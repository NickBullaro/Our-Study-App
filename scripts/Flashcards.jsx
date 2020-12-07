import * as React from 'react';
import ReactDOM from 'react-dom';
import { v4 as uuidv4 } from 'uuid';
import PropTypes from 'prop-types';
import FlashcardTest from './FlashcardTest';
import Flashcard from './Flashcard';

import Socket from './Socket';


export default function Flashcards() {
  const [addCards, setAddCards] = React.useState(false);
  const [flashcards, setFlashcards] = React.useState([]);
  const [popOut, setPop] = React.useState(false);
 

  const CARDS = 'cards';

  function togglePop() {
   setPop(!popOut);
  }
  function addFlashCards(e) {
    e.preventDefault();
    setAddCards(true);
  }

  function newCards() {
    React.useEffect(() => {
      Socket.on(CARDS, (data) => {
        setFlashcards(data);
      });
    });
  }
  function showTest() {
  
  /*let new_window = window.open('', '_blank', 'height=500px, width=800px');
  
  
 
  
  new_window.document.title = 'Room Test';
 /* 
  let script1 = document.createElement('script');
  let link1 = document.createAttribute('link');
  let link2 = document.createElement('link');
  let script2 = document.createElement('script');
  let script3 = document.createElement('script');
  let script4 = document.createElement('script');
  
  
  
  link1.rel = link2.rel = 'stylesheet';
  link1.href = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css";
  link1.integrity = "sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z";
  link1.crossorigin = 'anonymous';
  link2.href = "/static/styles.css";
  
  
  script1.src = '/static/script.js';
  
  
  script2.src = "https://code.jquery.com/jquery-3.5.1.slim.min.js";
  script2.integrity = "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj";
  script2.crossorigin = 'anonymous';
  
  script3.src = "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js";
  script3.integrity = "sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN";
  script3.crossorigin = 'anonymous';
  
  script4.src = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js";
  script4.integrity = "sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV";
  script4.crossorigin = 'anonymous';
  
  script4.type = script3.type = script2.type = script1.type = 'text/javascript';
  
  //document.head.appendChild(link1);
  //document.head.appendChild(link2);
  
  document.head.appendChild(script1);
  document.head.appendChild(script2);
  document.head.appendChild(script3);
  document.head.appendChild(script4);
  


   
  let div = new_window.document.createElement('div');
  div.id = 'test';
  new_window.document.body.append(div);
  
  ReactDOM.render(<FlashcardTest cards={flashcards}/>, new_window.document.getElementById('test') );
  */
  var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
  
}
  
  // Get the modal

  newCards();

  return (
    addCards
      ? <CreateFlashcards cards={flashcards} />
      : (
          <div>
          
          
      
          <div id="myModal" className="modal">
          
            <div className="modal-content">
              <span className="close">&times;</span>
              <FlashcardTest />
            </div>
          
          </div>
          <div>
            <div className="card-grid" id='cards'>
              {flashcards.map((flashcard) => <Flashcard key={uuidv4()} flashcard={flashcard} />)}
            </div>
            <button type="submit" onClick={addFlashCards}>Edit Flashcards</button>
            <button id='myBtn' onClick={showTest}> Test Me </button>
          </div>
          </div>
      )
  );
}

function CreateFlashcards({ cards }) {
  const [submitted, setSubmit] = React.useState(false);
  const [fields, setFields] = React.useState(cards);
  const NEW_CARDS = 'new cards';

  function handleQuestion(i, event) {
    const values = [...fields];
    values[i].question = event.target.value;
    setFields(values);
  }

  function handleAnswer(i, event) {
    const values = [...fields];
    values[i].answer = event.target.value;
    setFields(values);
  }

  function handleAdd() {
    const values = [...fields];
    values.push({ question: '', answer: '' });
    setFields(values);
  }

  function handleRemove(i) {
    const values = [...fields];
    values.splice(i, 1);
    setFields(values);
  }

  function handleSubmit(event) {
    event.preventDefault();
    Socket.emit(NEW_CARDS, fields);
    setSubmit(true);
  }

  return (
    submitted
        ? <Flashcards />
        : (
            <div id="editing_cards" className="container">
                <div id="flashcards_editor">
                    {fields.map((field, idx) => (
                    <div key={`${field + idx}`} className="form_row">
                        <input type="text" className="question" placeholder="Enter question" value={field.question} onChange={(e) => handleQuestion(idx, e)} />
                        <input type="text" className="answer" placeholder="Enter answer" value={field.answer} onChange={(e) => handleAnswer(idx, e)} />
                        <button type="button" onClick={() => handleRemove(idx)}>X</button>
                    </div>
                    ))}
                </div>
                <div className="flashcard_button_row">
                    <button type="button" id="addCard" onClick={handleAdd}>Add Card</button>
                    <button type="button" onClick={handleSubmit}>Done</button>
                </div>
            </div>
        )
  );
}

CreateFlashcards.defaultProps = {
  cards: [],
};

CreateFlashcards.propTypes = {
  cards: PropTypes.arrayOf(PropTypes.object),

};
