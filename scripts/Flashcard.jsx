import React, { useState } from 'react';
import './styles.css';
export default function Flashcard({ flashcard }) {
    
    const [flip, setFlip] = useState(false);
    
    function flipCard(){
        setFlip(!flip);
    }
    
    return (
        <div className={`card ${ flip ? "flip" : '' } `} onClick={flipCard}>
        
        <div className='front'>
            {flashcard.question}
            <div className='flashcard-options'>
                {flashcard.options.map( option => {
                    return <div className='flashcard-option'>{option}</div>
                })}
            </div>
        </div>
        
        <div className='back'>{flashcard.answer}</div>
        
        { flip ? flashcard.answer : flashcard.question}
        </div>
    );
}