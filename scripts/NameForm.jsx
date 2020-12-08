import * as React from 'react';

function NameForm({ myRef }) {
  return (
    <label htmlFor="new">
      New Board:
      <input id="new" name="new" type="text" ref={myRef} />
    </label>
  );
}
export default NameForm;
