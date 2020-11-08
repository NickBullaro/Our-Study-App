import React, { useState } from 'react';

function Flashcard({ flashcard }) {
  const [flip, setFlip] = useState(false);

  function flipCard() {
    setFlip(!flip);
  }

  return (
    <div
      className={`flashcard ${flip ? 'flip' : ''} `}
      onClick={flipCard}
    >

      <div className="front">
        {flashcard.question}
        <div className="flashcard-options">
          {flashcard.options.map((option) => <div className="flashcard-option">{option}</div>)}
        </div>
      </div>

      <div className="back">{flashcard.answer}</div>
    </div>
  );
}

export default Flashcard;
