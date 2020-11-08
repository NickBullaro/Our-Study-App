import React, { useState } from 'react';
import Flashcard from './Flashcard';
import Socket from './Socket';

const SAMPLE_CARDS = [
  {
    id: 1,
    question: 'Question 1 ',
    answer: 'Answer 1',
    options: ['option1', 'option2', 'option3'],
  },
  {
    id: 2,
    question: 'Question 2 ',
    answer: 'Answer 2',
    options: ['answer1', 'nome', 'smac'],
  },
];

function Flashcards() {
  const [flashcards, setFlashcards] = useState(SAMPLE_CARDS);

  function setup() {
    React.useEffect(() => {
      Socket.on('sending room data', (data) => {
        setFlashcards(data.flashcardList);
      });
    });
  }

  setup();

  return (
    <div className="card-grid">
      {flashcards.map((flashcard) => <Flashcard key={flashcard.id} flashcard={flashcard} />)}

    </div>
  );
}

export default Flashcards;
