import React, { useState } from 'react';

export default function FlashCards() {
    const [flashcards, setFlashcards] = useState(SAMPLE_CARDS);
    
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
        
        
        ]
    
    return {
        <div>
        
        
        </div>
    }
}