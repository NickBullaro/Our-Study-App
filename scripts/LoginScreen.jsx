import * as React from 'react';
import Socket from './Socket';
import { GoogleButton } from './GoogleButton';

function LoginScreen() {
  
  function fakeLogin() {
    Socket.emit('new user login', {
      msg: ""
    });
  }

  return (
    <div id='loginScreen'>
        <p>Insert Login Screen HTML and components here</p>
        <h1>Sign in with Google to continue!</h1>
        <GoogleButton/>
    </div>
  );
}

export default LoginScreen;
