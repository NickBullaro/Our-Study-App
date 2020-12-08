import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';


function LoginScreen() {
  return (
    <div id="loginScreen">
     <h1>Chatbox</h1>
      <h2>Sign in with Google to continue!</h2>
      <GoogleButton />
      <FacebookButton />
    </div>
  );
}

export default LoginScreen;
