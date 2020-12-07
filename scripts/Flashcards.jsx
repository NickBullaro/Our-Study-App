import * as React from 'react';
import { v4 as uuidv4 } from 'uuid';
import PropTypes from 'prop-types';
import FlashcardTest from './FlashcardTest';
import Flashcard from './Flashcard';

import Socket from './Socket';

export default function Flashcards() {
  const [addCards, setAddCards] = React.useState(false);
  const [flashcards, setFlashcards] = React.useState([]);

  const CARDS = 'cards';

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
    const modal = document.getElementById('myModal');
    const span = document.getElementsByClassName('close')[0];

    modal.style.display = 'block';

    span.onclick = () => {
      modal.style.display = 'none';
    };

    window.onclick = (event) => {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    };
  }

  newCards();

  return (
    addCards
      ? <CreateFlashcards cards={flashcards} />
      : (
        <div>

          <div id="myModal" className="modal">

            <div className="modal-content">
              <span className="close">&times;</span>
              <FlashcardTest cards={flashcards} />
            </div>

          </div>
          <div>
            <div className="card-grid" id="cards">
              {flashcards.map((flashcard) => <Flashcard key={uuidv4()} flashcard={flashcard} />)}
            </div>
            <button type="submit" onClick={addFlashCards}>Edit Flashcards</button>
            <button type="button" id="takeTest" onClick={showTest}> Test Me </button>
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
