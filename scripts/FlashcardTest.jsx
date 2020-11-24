import React, { useState, useEffect } from 'react';
import Socket from './Socket';

const TEST_FLASHCARDS  = [
      {
          "question" : '2+2=',
          "answer" : '4'
      },
      
       {
          "question" : "What is the capital of NJ?",
          "answer" : 'Trenton'
      },
      
       {
          "question" : 'Who is the first US President',
          "answer" : 'George Washington'
      },
      
       {
          "question" : 'Who is the best person in the world',
          "answer" : 'Definitely You :)'
      },
      ];
      
export default function FlashcardTest() {
    
    const [flashcards, setFlashcards] = useState(TEST_FLASHCARDS);
    const [key, setKey] = useState([]);
    const [test, setTest] = useState([{}]);
    const [result, setResult] = useState([]);
    const [fields, setFields] = useState([]);
    const [correct, setCorrect] = useState(false);
    
    const QUIZ_ANSWERS = 'quiz answers';
    const NEW_CARDS = 'new cards';
    const QUIZ_RESULT = 'quiz result';

  function handleAnswer(i, event) {
    const values = [...fields];
    values[i] = event.target.value;
    setFields(values);
  
  }


    function shuffle(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;
    
      // While there remain elements to shuffle...
      while (0 !== currentIndex) {
    
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
    
        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }
    
      return array;
    }
    
    function handleSubmit(event) {
    event.preventDefault();
    if (fields.length == test.length){
        console.log("All answers filled");
        Socket.emit(QUIZ_ANSWERS, [key, fields]);
   
    }
    else {
        alert("You did not fill out the quiz");
    }
  }
    
    function setUp() {
        React.useEffect( () => {
        Socket.emit(NEW_CARDS, flashcards);    
        
        
        let answers = [];
        let questions = [];
        
        for (let i = 0; i < flashcards.length; i++) {
            questions.push(flashcards[i].question);
            answers.push(flashcards[i].answer);
           
        }
        
        shuffle(questions);
        shuffle(answers);

        let tests = [];
        let answer_key = [];
        for(let i = 0; i < flashcards.length; i++){
            let test = {'question' : questions[i], 'answer': answers[i]};
            answer_key.push(
                {
                    'answer' : flashcards.find( ({ question }) => question === questions[i] ).answer, 
                    'question' : questions[i],
                }
            
            );
           
            tests.push(test);
        }
  
        setTest(tests);
        setKey(answer_key);
     
    }, [flashcards]);
    }
    
    function checkQuiz() {
        useEffect( () => {
           Socket.on(QUIZ_RESULT, data => {
               console.log("Res:",result);
               for(let i in data){
                   if (data[i] == 1){
                       result[i] = true;
                   }
                   else{
                       result[i] = false;
                   }
               }
               
             setResult(result);  
           });
        }, [result]);
    }
    
    checkQuiz();
    setUp();
  return (
   <div>
    Possible Answers  
   {
   test.map( (flashcard, index) =>
   <div>
                
            <div className='row'>
                <div className='col-12'>
                    <p>{flashcard.answer}</p>
                </div>
            </div>
    </div>
       )
   }
     <div>
        Answer the following questions:
        <br/>
        <form>
            {test.map((field, idx) => (
              <div key={`${field + idx}`} className="form-row">
             
                <div className='col-5'>
                    <label htmlFor='answer'>{field.question}</label>
                
                </div>
      
                <div className="col-5">
                   <input type="text" className={`answer ${result[idx] ? 'correct' : '' }`} placeholder="Enter answer" onChange={(e) => handleAnswer(idx, e)} />
                      
                  
                </div>
            
                
              </div>
            ))}
            
            <input type='button' value="Submit quiz" onClick={handleSubmit} />
        </form>
            
    </div>
    
    </div>
     );  
   }
