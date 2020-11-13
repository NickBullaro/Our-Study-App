import * as React from 'react';
import GoogleButton from './GoogleButton';

function LoginScreen() {
  return (
    <div id="loginScreen">
     <h1>Chatbox</h1>
      <h2>Sign in with Google to continue!</h2>
      <GoogleButton />
    </div>
  );
}

export default LoginScreen;
