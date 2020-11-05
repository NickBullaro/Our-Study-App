import React, { useState } from 'react';
import Socket from './Socket';
import CreateFlashcard from './CreateFlashcard';

export default function CreateFlashcards ({ oldEntries }) {
    
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [entries, setEntries] = useState(oldEntries);

    
    function handleSubmit(event){
        event.preventDefault();
        console.log(entries);
        Socket.emit('new cards', entries);
    }
    
    function addCard(){
        const entry = {
            'question': question,
            'answer': answer
        };
        setEntries([...entries, entry]);
        console.log(entries);
        
        
    }
    return (
        <div>
            <h2>Create Flashcards</h2>
            
            <form onSubmit={handleSubmit}>
              <CreateFlashcard oldEntries={oldEntries} addCard={addCard} handleSubmission={handleSubmit} question={setQuestion} answer={setAnswer} />
            
                <button type='submit'>Done</button>
            </form>
        
        </div>
        );
}