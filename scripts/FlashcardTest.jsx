import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Socket from './Socket';

export default function FlashcardTest({ cards }) {
  const [key, setKey] = useState([]);
  const [test, setTest] = useState([{}]);
  const [flashcards, setFlashcards] = useState(cards);

  const [fields, setFields] = useState([]);

  const CARDS = 'cards';

  function handleAnswer(i, event) {
    const values = [...fields];
    values[i] = event.target.value;
    setFields(values);
  }

  function shuffle(arr) {
    const array = [...arr];

    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * i);
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }

    return array;
  }
  function newCards() {
    useEffect(() => {
      Socket.on(CARDS, (data) => {
        setFlashcards(data);
      });
    });
  }

  function checkQuiz() {
    for (let i = 0; i < fields.length; i += 1) {
      const field = document.getElementById(`field${i}`);
      if (key[i].answer.toLowerCase() === fields[i].toLowerCase()) {
        field.className = 'answer form-control correct';
      } else {
        field.className = 'answer form-control wrong';
      }
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (fields.length === test.length) {
      checkQuiz();
    } else {
      alert('You did not fill out the quiz');
    }
  }

  function setUp() {
    React.useEffect(() => {
      let answers = [];
      let questions = [];

      for (let i = 0; i < flashcards.length; i += 1) {
        questions.push(flashcards[i].question);
        answers.push(flashcards[i].answer);
      }

      questions = shuffle(questions);
      answers = shuffle(answers);

      const tests = [];
      const answerKey = [];
      for (let i = 0; i < flashcards.length; i += 1) {
        const tempTest = { question: questions[i], answer: answers[i] };
        answerKey.push(
          {
            answer: flashcards.find(({ question }) => question === questions[i]).answer,
            question: questions[i],
          },

        );

        tests.push(tempTest);
      }

      setTest(tests);
      setKey(answerKey);
    }, [cards]);
  }

  newCards();
  setUp();

  return (
    <div>
      Possible Answers
      {
   test.map((flashcard, index) => (
     <div key={`${flashcard + index}`}>

       <div className="row">
         <div className="col-12">
           <p>{flashcard.answer}</p>
         </div>
       </div>
     </div>
   ))
   }
      <div>
        Answer the following questions:
        <br />
        <form>
          {test.map((field, idx) => (
            <div key={`${field + idx}`} className="form-row">

              <div className="col-5">
                <label htmlFor="answer">{field.question}</label>

              </div>

              <div className="col-5 input-group mb-3">
                <input type="text" className="answer form-control" id={`field${idx}`} placeholder="Enter answer" onChange={(e) => handleAnswer(idx, e)} />

              </div>

            </div>
          ))}

          <input type="button" value="Submit quiz" onClick={handleSubmit} />

        </form>

      </div>

    </div>
  );
}

FlashcardTest.defaultProps = {
  cards: [],
};

FlashcardTest.propTypes = {
  cards: PropTypes.arrayOf(PropTypes.object),

};
