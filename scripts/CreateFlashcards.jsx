import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import Socket from './Socket';
import Flashcards from './Flashcards';

export default function CreateFlashcards({ cards }) {

  const [submitted, setSubmit] = useState(false);
  const [fields, setFields] = useState(cards);
  const NEW_CARDS = 'new cards';
  
  function handleQuestion(i, event) {
    const values = [...fields];
    values[i].question = event.target.value;
    setFields[values];
  }
  
  function handleAnswer(i, event) {
    const values = [...fields];
    values[i].answer = event.target.value;
    setFields[values];
  }
  
  function handleAdd() {
    /*event.preventDefault();
    const entry = {
      question: question,
      answer: answer,
    };
    Socket.emit('new card', entry);*/
    
    const values = [...fields];
    values.push({ question: null, answer: null });
    setFields(values);
    console.log(values);
  }
  
  function handleRemove(i) {
    const values = [...fields];
    values.splice(i, 1);
    setFields(values);
  }
  
  function handleSubmit(event) {
    event.preventDefault();
    Socket.emit(NEW_CARDS, fields);
    setSubmit(true);
  }
  
  
  return (
    submitted ?  
    <Flashcards />
    :
    <div>
      <form method='POST' onSubmit={handleSubmit} > 
        <h2>Create Flashcards</h2>
          {fields.map((field, idx) => {
        return (
          <div key={`${field}-${idx}`} className="row">

            <div className="col-4" >
              <input type="text" className='question' placeholder="Enter question" value={field.question} onChange={e => handleQuestion(idx, e)}  name={ `question${idx}` } required />
            </div>
            <div className="col-4">
              <input type="text" className='answer' placeholder="Enter answer" value={field.answer} onChange={e => handleAnswer(idx, e)}  name={ `answer${idx}` } required />
            </div>
            <div className="col-2">
              <button type="button" onClick={() => handleRemove(idx)}>X</button>
            </div>
            <div className="col-1" />
          </div>
        );
      })}
                  
        <div className='row'>
          <span>  
            <button type='button' id='addCard' onClick={handleAdd}>Add Card</button>
          </span>
          
        </div>
              
  
        <input type="submit" value='Done'  />
      </form>
    </div>
  );
}
