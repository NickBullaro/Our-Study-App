import * as React from 'react';

import { GoogleButton } from './GoogleButton';
import { Socket } from './Socket';



export function Login() {
    
    
    
    return (
    <div className="joinOuterContainer">
        <div className="joinInnerContainer">
        <h3 className="heading">Sign in with Google to continue!</h3>
            <GoogleButton/>
        </div>
    </div>
    );
}