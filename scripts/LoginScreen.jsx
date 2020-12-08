import * as React from 'react';
import GoogleButton from './GoogleButton';

function LoginScreen() {
  return (
    <div id="loginScreen">
      <h2>Sign in with Google!</h2>
      <GoogleButton />
    </div>
  );
}

export default LoginScreen;
