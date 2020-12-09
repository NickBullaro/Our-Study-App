import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';


function LoginScreen() {
  return (
    <div id="loginScreen">
      <h2>Sign in with Google!</h2>
      <GoogleButton />
      <FacebookButton />
    </div>
  );
}

export default LoginScreen;
