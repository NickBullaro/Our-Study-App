import * as React from 'react';
import * as ReactDOM from 'react-dom';
import Content from './Content';


function LandingPage() {
    function redirectPage() {
        ReactDOM.render(<Content />, document.getElementById('main'));
    }
function openTab(event) {
    document.getElementById('ourApp').style.display = 'none';
    document.getElementById('aboutUs').style.display = 'none';
    document.getElementById('appMethodology').style.display = 'none';
        
    if (event.target.id === "aboutBtn"){
        document.getElementById('ourApp').style.display = 'block';
    }
    
    if (event.target.id === "aboutUsBtn"){
        document.getElementById('aboutUs').style.display = 'block';
    }
    if (event.target.id === "appMethodologyBtn"){
        document.getElementById('appMethodology').style.display = 'block';
    }
    
}
    return (
        <div id='welcome'>
            <div id="landingPage" className="row LandingPage">
                <div className="welcomeMessage"> Welcome to Our Study! </div>
            </div>
            <div className='row landingButtons'>
                <button type='button' onClick={openTab} id='aboutBtn' className='btn btn-primary'>About our App </button>
                <button type='button' onClick={openTab} id='aboutUsBtn' className='btn btn-primary'>About Us </button>
                <button type='button' onClick={openTab} id='appMethodologyBtn' className='btn btn-primary'>Our App Methodology </button>
            </div>
            <div className='row'>
                <div id='aboutUs'>
                    <div className='landingQuestion'>Who are we?</div>
                    <div className="whoWeAre">
                        <p>We are Group 7!</p>
                        <p>Our group members are Jason Molisani, Navado Wray, Mitchell Mecca, George Alvarado, and Nick Bullaro.</p>
                        <p>We are all seniors at NJIT interested in persuing a career in software engineering.</p>
                        <p>As part of our Design in Software Engineering class, we created this web app to demonstrate the core concepts we have learned so far.</p>
                    </div>
                </div>
                    <div id='ourApp'>
                    <div className='landingQuestion'>What did we make?</div>
                    <div className="whatWeMade">
                        <p>Our web app is a collaborative study app. We combined Zoom, Google Drawing, and Quizlet Flashcards into one easy-to-use app!</p>
                    </div>
                    </div>
            
                <div id='appMethodology'>
                    <div className='landingQuestion'>How did we make our app?</div>
                    <div className="whatWeUsed" >
                        <p className="backend">We made this app through full-stack development.</p>
                        <p className="backend">We used python, Socketio, Flask, SQLAlchemy, and Postgres 
                            in the backend to make our app function the way it's supposed to.</p>
                        <p className="frontend">We used Javascript, React, HTML, CSS, and more in the front-end to make our app show what it needed to and look pretty!</p>
                        <p>We also used Google and Facebook Oauth for access control and Twilio Video for our audio/video streaming.</p>
                    </div>
                </div>
            </div>
            <div className="tryIt">Wanna try it out?</div>
            <div className="whereItIs">
                <p className="loadingButton">To be redirected to the login page, you can click this button!</p>
            </div>
            <div>
                <button className="redirectButton btn btn-primary" type="button" onClick={redirectPage}>Head to the app!</button>
            </div>
        </div>
  );
}

export default LandingPage;
