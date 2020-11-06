import React from 'react';
import * as ReactDOM from 'react-dom';

import Socket from './Socket';
import { GoogleLogin } from 'react-google-login';
import { Content } from './Content';


const responseGoogle = (response) => {
  console.log(response);
}

function handleSubmit(response) {
    console.log(response.profileObj)
    console.log(response.profileObj.name);
    console.log(response.profileObj.email);
    let user = response.profileObj.name;
    let email = response.profileObj.email;
    let pic = response.profileObj.imageUrl;
    Socket.emit("new user login", {
        'user': user,
        'email': email,
        'pic': pic
    });
    
    console.log('Sent the name ' + user + ' to server!');
    console.log('Sent the email ' + email + ' to server!');
    console.log('Sent the pic ' + pic + ' to server!');
    ReactDOM.render(<LoggedInContent/>, document.getElementById('content'));
}




export function GoogleButton() {
    return (
                <GoogleLogin
                className="gbutton"
                clientId="734948163476-c023m7n67lmmk5dobh85ank7b56o6477.apps.googleusercontent.com"
                buttonText="Login"
                onSuccess={handleSubmit}
                onFailure={responseGoogle}
                cookiePolicy={'single_host_origin'}/>
            );
}

 
