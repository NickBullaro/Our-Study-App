import React, { useState } from 'react';

export default function Flashcard({ flashcard }) {
    
    const [flip, setFlip] = useState(false);
    
    function flipCard(){
        setFlip(!flip);
    }
    function deleteCard() {
        console.log('Delete card');
    }
    
    return (
        <div 
        className={`flashcard ${ flip ? "flip" : '' } `} 
        onClick={flipCard}
        >
            <div>
                <img src="https://cdn3.iconfinder.com/data/icons/ui-essential-elements/110/DeleteDustbin-512.png" className='trash' onClick={deleteCard} />
            </div>
        <div className='front'>{flashcard.question}</div>
        
        <div className='back'>{flashcard.answer}</div>
        </div>
    );
}


/*<div className='flashcard-options'>
                {flashcard.options.map( option => {
                    return <div className='flashcard-option'>{option}</div>;
                })}
            </div>*/
            