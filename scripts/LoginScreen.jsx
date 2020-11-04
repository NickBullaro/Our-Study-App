import * as React from 'react';
import Socket from './Socket';

function LoginScreen() {
  
  function fakeLogin() {
    Socket.emit('new user login', {
      msg: ""
    });
  }

  return (
    <div id='loginScreen'>
        <p>Insert Login Screen HTML and components here</p>
        <button onClick={ fakeLogin }>FakeLogin</button>
    </div>
  );
}

export default LoginScreen;
