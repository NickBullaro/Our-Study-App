import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Flashcard from './Flashcard';
import CreateFlashcards from './CreateFlashcards';
import Socket from './Socket';

export default function Flashcards() {
  const [addCards, setAddCards] = useState(false);
  const [flashcards, setFlashcards] = useState([]);

  const CARDS = 'cards';

  function addFlashCards(e) {
    e.preventDefault();
    setAddCards(true);
  }

  function newCards() {
    useEffect(() => {
      Socket.on(CARDS, (data) => {
        setFlashcards(data);
      });
    });
  }

  newCards();

  return (
    addCards
      ? <CreateFlashcards cards={flashcards} />
      : (
        
          <div className="card-grid">
            {flashcards.map((flashcard) => <Flashcard key={uuidv4()} flashcard={flashcard} />)}
            <button type="submit" onClick={addFlashCards}>Edit Flashcards</button>
          </div>
      )
  );
}
