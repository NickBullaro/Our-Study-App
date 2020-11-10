import React, { useState, useEffect } from 'react';
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
    
    function new_cards() {
    useEffect( () => {
      Socket.on(CARDS, data => {
        console.log(data);
        setFlashcards(data);
      });
    });
  }
  
  
  new_cards();
  
    return (
        addCards ?
        <CreateFlashcards cards={flashcards} /> 
        :
        <div>
            <div className='card-grid'>
            {flashcards.map( flashcard => {
                return <Flashcard key={flashcard.id} flashcard={flashcard} />;
            })
            }
            <button type='submit' onClick={addFlashCards}>Edit Flashcards</button> 
            </div>
        </div>
    );
}