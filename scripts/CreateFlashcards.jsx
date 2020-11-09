import React, { useState, useEffect } from 'react';
import Socket from './Socket';
import Flashcards from './Flashcards';

export default function CreateFlashcards() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmit] = useState(false);
  
  function addCard() {
    const entry = {
      question: question,
      answer: answer,
    };
    Socket.emit('new card', entry);
  }
  
  function handleSubmit(event) {
    event.preventDefault();
    setSubmit(true);
  }
    
  return (
    submitted ?  
    <Flashcards />
    :
    <div>
      <h2>Create Flashcards</h2>
        <div className='row'>
                <div className='col-6'>
                    <input type='text' id='question' onChange={ (event) => setQuestion(event.target.value) } />
                </div>
                <div className='col-6'>
                    <input type='text' id='answer' onChange={ (event) => setAnswer(event.target.value) } />
                </div>
            </div>
            
            <div className='row'>
                <span>  
                    <button type='button' onClick={addCard}>Add Card</button>
                </span>
            </div>

            <button type="button" onClick={handleSubmit}>Done</button>

    </div>
  );
}
