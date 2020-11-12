import React, { useState } from 'react';
import PropTypes from 'prop-types';

export default function Flashcard({ flashcard }) {
  const [flip, setFlip] = useState(false);

  function flipCard() {
    setFlip(!flip);
  }

  return (
    <button
      type="button"
      className={`flashcard ${flip ? 'flip' : ''} `}
      onClick={flipCard}

    >
      <div className="front">{flashcard.question}</div>

      <div className="back">{flashcard.answer}</div>
    </button>
  );
}

Flashcard.defaultProps = {
  flashcard: {},
};

Flashcard.propTypes = {
  flashcard: PropTypes.shape({
    question: PropTypes.string.isRequired,
    answer: PropTypes.string.isRequired,

  }),

};
