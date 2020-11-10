import * as React from 'react';
import LoggedInContent from './LoggedInContent';
import LoginScreen from './LoginScreen';
import Socket from './Socket';
import Whiteboard from './Whiteboard'

function Content() {
  const [loggedIn, setLoginState] = React.useState(false);

  function setup() {
    React.useEffect(() => {
      Socket.on('login accepted', () => {
        setLoginState(true);
      });
    });
  }

  setup();

  return (
    <div id="content">
      {
        loggedIn
          ? <LoggedInContent />
          : <LoginScreen />
      }
      <Whiteboard />
    </div>
  );
}

export default Content;
