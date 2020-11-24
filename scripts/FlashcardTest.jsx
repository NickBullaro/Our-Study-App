import React, { useState, useEffect } from 'react';

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
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState([]);
    const [numberOfCards, setCardLength] = useState(0);
    const [test, setTest] = useState([{}]);
    
    const [fields, setFields] = useState([TEST_FLASHCARDS]);
 

  function handleQuestion(i, event) {
    const values = [...fields];
    values[i].question = event.target.value;
    setFields(values);
  }

  function handleAnswer(i, event) {
    const values = [...fields];
    values[i].answer = event.target.value;
    setFields(values);
  }

  function handleAdd() {
    const values = [...fields];
    values.push({ question: '', answer: '' });
    setFields(values);
  }

  function handleRemove(i) {
    const values = [...fields];
    values.splice(i, 1);
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
    
    function setUp() {
        React.useEffect( () => {setFlashcards(shuffle(flashcards));
        let i = 0;
        var answers = [];
        var questions = [];
        for (i; i < flashcards.length; i++) {
            questions.push(flashcards[i].question);
            answers.push(flashcards[i].answer);
        }
        
        shuffle(questions);
        shuffle(answers);
        setQuestions(questions);
        setAnswers(answers);
        var tests = [];
        for(let i = 0; i < flashcards.length; i++){
            let test = {'question' : questions[i], 'answer': answers[i]};
            tests.push(test);
        }
        
        setTest(tests);
        setCardLength(tests.length);
        
    }, [flashcards]);
    }
    
    console.log(flashcards);
    setUp();
    //React.useEffect( () => setUp());//setFlashcards(shuffle(flashcards)));
    
    for(let i = 0; i < numberOfCards; i++){
        console.log(String.fromCharCode(i+97));
    }

  return (
   <div>
    
   {
   test.map( (flashcard, index) =>
   <div>
              
            <div className='row'>
                <div className='col-5'>
                    <p>{(index+1) + ".  " + flashcard.question}</p>
                </div>
                <div className='col-5'>
                    <p>{String.fromCharCode(97+index) + ".  " +  flashcard.answer}</p>
                </div>
            </div>
    </div>
       )
   }
     <div>
        Answer the following questions:
            {/*fields.map((field, idx) => (
              <div key={`${field + idx}`} className="form-row">
  
                <div className="col-5">
                  <input type="text" className="question" placeholder="Enter question" value={field.question} onChange={(e) => handleQuestion(idx, e)} />
                </div>
                <div className="col-5">
                  <input type="text" className="answer" placeholder="Enter answer" value={field.answer} onChange={(e) => handleAnswer(idx, e)} />
                </div>
  
                <button type="button" onClick={() => handleRemove(idx)}>X</button>
  
              </div>
            ))}*/
            }
    </div>
    
    </div>
     );  
   }
