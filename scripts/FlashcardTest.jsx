import React, { useState, useEffect } from 'react';
import Socket from './Socket';
import InRoomScreen from './InRoomScreen';
import PropTypes from 'prop-types';

const TEST_FLASHCARDS = [
  {
    question: '2+2=',
    answer: '4',
  },

  {
    question: 'What is the capital of NJ?',
    answer: 'Trenton',
  },

  {
    question: 'Who is the first US President',
    answer: 'George Washington',
  },

  {
    question: 'Who is the best person in the world',
    answer: 'Definitely You :)',
  },
];

export default function FlashcardTest() {
  // const [flashcards, setFlashcards] = useState(TEST_FLASHCARDS);
  const [key, setKey] = useState([]);
  const [test, setTest] = useState([{}]);
  const [flashcards, setFlashcards] = useState([]);
  
  const [home, setHome] = useState(false);
  const [fields, setFields] = useState([]);
  
  const CARDS = 'cards';

  function handleAnswer(i, event) {
    const values = [...fields];
    values[i] = event.target.value;
    setFields(values);
  }

  function shuffle(arr) {
    let currentIndex = arr.length;
    let temporaryValue;
    let randomIndex;
    const array = [...arr];

    // While there remain elements to shuffle...
    while (currentIndex !== 0) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
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
      const answers = [];
      const questions = [];

      for (let i = 0; i < flashcards.length; i += 1) {
        questions.push(flashcards[i].question);
        answers.push(flashcards[i].answer);
      }
      console.log(flashcards);

      shuffle(questions);
      shuffle(answers);

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
    }, [flashcards]);
  }
  
  
  newCards();
  setUp();
  
  return (
    <div>
      Possible Answers
      {
   test.map((flashcard, index) => (
     <div>

       <div className="row" key={`${flashcard + index}`}>
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
  flashcards: [],
};

FlashcardTest.propTypes = {
  flashcards: PropTypes.arrayOf(PropTypes.object),

};
