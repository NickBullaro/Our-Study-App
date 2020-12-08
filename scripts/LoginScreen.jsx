import * as React from 'react';
import GoogleButton from './GoogleButton';

function LoginScreen() {
  function Refresh() {
    return;
  }
  return (
    <div id="loginScreen">
      <p id="about_link"><a href="about.html"> About Our Study </a></p>
      <button id="refresh_button" onClick={Refresh} type="submit"><img src="/static/refresh_icon.jpg" id="refresh_image"/></button>
      <h1>Our Study</h1>
      <h2>Sign in with Google to continue!</h2>
      <GoogleButton />
    </div>
  );
}

export default LoginScreen;
