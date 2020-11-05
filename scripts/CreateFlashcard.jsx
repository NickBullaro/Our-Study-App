import React, { useState } from 'react';
import Socket from './Socket';


export default function CreateFlashcard ({ oldEntries, addCard, handleSubmission, question, answer } ) {
    
    return (
        <div>
            {oldEntries.map( entry => {
            
            return(
                <div className='row'>
                    <div className='col-6'>
                        <input type='text' id='question' value={entry.question}/>
                    </div>
                    <div className='col-6'>
                        <input type='text' id='answer' value={entry.answer} />
                    </div> 
                </div>
                );
            })
            }
            <div className='row'>
                <div className='col-6'>
                    <input type='text' id='question' onChange={ (event) => question } />
                </div>
                <div className='col-6'>
                    <input type='text' id='answer' onChange={ (event) => answer } />
                </div>
            </div>
            
            <div className='row'>
                <span>  
                    <button type='button' onClick={addCard}>Add Card</button>
                </span>
            </div>
        
        </div>
        );
}