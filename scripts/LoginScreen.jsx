import * as React from 'react';
import GoogleButton from './GoogleButton';

function LoginScreen() {
  return (
    <div id="loginScreen">
      <h1>Sign in with Google to continue!</h1>
      <GoogleButton />
    </div>
  );
}

export default LoginScreen;
