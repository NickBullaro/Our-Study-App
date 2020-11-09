import React, { useState } from 'react';
import Flashcard from './Flashcard';
import Socket from './Socket';

function Flashcards() {
  const [flashcards, setFlashcards] = useState([]);

  function setup() {
    React.useEffect(() => {
      Socket.on('sending room data', (data) => {
        console.log("updating flashcards")
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
