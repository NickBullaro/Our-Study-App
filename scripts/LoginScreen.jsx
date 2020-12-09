import * as React from 'react';
import GoogleButton from './GoogleButton';

function LoginScreen() {
  function Refresh() {
    return;
  }
  return (
    <div id="loginScreen">
      <button id="refresh_button" onClick={Refresh} type="submit">
        <img id="refresh_image" alt="" src="../static/refresh_icon.jpg"/>
      </button>
      <form action="about.html" id="help">
        <button type="submit">?</button>
      </form>
      <div id="about_help">About us</div>
      <h1>Our Study</h1>
      <h2>Sign in with Google to continue!</h2>
      <GoogleButton />
    </div>
  );
}

export default LoginScreen;
