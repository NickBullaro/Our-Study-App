import React from 'react';
import FacebookLogin from 'react-facebook-login';
import Socket from './Socket';

const responseFacebook = (response) => {
  console.log(response);
};
 


export default function FacebookButton() {
  
  function handleSubmit(response) {
  console.log(response);
  console.log(response.name);
  console.log(response.email);
  console.log(response.picture.data.url);
  const user = response.name;
  const email = response.email;
  const pic = response.picture.data.url;
  Socket.emit('facebook login', {
    user,
    email,
    pic,
  });

  console.log(`Sent the name ${user} to server!`);
  console.log(`Sent the email ${email} to server!`);
  console.log(`Sent the pic ${pic} to server!`);
}

  return (
    <FacebookLogin
      appId="2082526558546130"
      autoLoad={false}
      fields="name,email,picture"
      callback={handleSubmit} 
      onFailure={responseFacebook}
      />
);
}

