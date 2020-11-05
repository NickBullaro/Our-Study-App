import React, { useState } from 'react';
import Flashcard from './Flashcard';

 const SAMPLE_CARDS = [
        {
            id: 1,
            question: "Question 1 ",
            answer: 'Answer 1',
            options: ['option1', 'option2', 'option3']
        },
        {
            id: 2,
            question: 'Question 2 ',
            answer: 'Answer 2',
            options: ['answer1', 'nome', 'smac']
        }
        
        
        ];
        
export default function Flashcards() {
    const [flashcards, setFlashcards] = useState(SAMPLE_CARDS);
    
        
    console.log(flashcards);
    
    return (
        <div className='card-grid'>
        {flashcards.map( flashcard => {
            return <Flashcard key={flashcard.id} flashcard={flashcard} />;
        })
        }
        
        </div>
    )
}