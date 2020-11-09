import React from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

const responseGoogle = (response) => {
  console.log(response);
};

function handleSubmit(response) {
  console.log(response.profileObj);
  console.log(response.profileObj.name);
  console.log(response.profileObj.email);
  const user = response.profileObj.name;
  const { email } = response.profileObj;
  const pic = response.profileObj.imageUrl;
  Socket.emit('new user login', {
    user,
    email,
    pic,
  });

  console.log(`Sent the name ${user} to server!`);
  console.log(`Sent the email ${email} to server!`);
  console.log(`Sent the pic ${pic} to server!`);
}

function GoogleButton() {
  return (
    <GoogleLogin
      className="gbutton"
      clientId="734948163476-c023m7n67lmmk5dobh85ank7b56o6477.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={handleSubmit}
      onFailure={responseGoogle}
      cookiePolicy="single_host_origin"
    />
  );
}

export default GoogleButton;
