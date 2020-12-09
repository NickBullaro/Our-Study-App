# Heroku Link: 'https://your-study.herokuapp.com'


# Contributors

- Jason Molisani
- Mitchell Mecca
- Nick Bullaro
- Navado Wray
- George Alvarado


# Getting Up and Running (do this once)
1. Clone this repository and navigate to the root folder within the terminal
2. Make sure you can execute the setup shell scripts with the following two lines:
   - `chmod 764 PSQLsetup.sh`
   - `chmod 764 reactSetup.sh`
3. Run the setup shell scripts:
   - `./PSQLsetup.sh`
   - `./reactSetup.sh`
4. Prep the resetup script:
   - `chmod 764 restart.sh`


# Getting Back Up and Running Locally (Do this every time other than the first)
1. In one terminal, navigate to the repository's root folder and execute `./restart.sh`
2. Leaving that running, open a second terminal, navigate to the root folder (again) and start the app with `python app.py`


# Individualized Information

1. Jason Molisani: 
    * Updated code skeleton to implement react and switch between 3 screens
      * Main
      * Content
      * InRoomScreen
      * LoggedInContent
      * LoginScreen
      * RoomSelectionScreen
      * Socket
    * Added room functionality and all related databases and components
      * Rooms DB
      * CurrentConnections DB
      * EnteredRooms DB
      * JoinedRooms DB
      * JoinedRoomsList
      * RoomJoinCreate
    * Set up tests
      * OnConnect
      * OnDisconnect

2. Mitchell Mecca: 
    * Create skeleton of webapp
    * Whiteboard component

3. Nick Bullaro: 
    * Created Landing Page and implemented functionality
        * LandingPage
        * Implemented HTML functionality
        * Implemented CSS beautification
    * Implemented Google Auth login functionality and created/edited related components
        * GoogleButton
        * LoginScreen (edited only- was created by Jason Molisani)
    * Created Chatbox functionality, created all related components, and edited related database tables
        * Messages table (edited only- created by Mitchell Mecca)
        * Chatbox
        * SendMessageButton
    * Implemented User List functionality and edited related component
        * UsersInRoomList (edited only- created by Jason Molisani)
    * Implemented video & audio streaming and created all related components
        * Stream
        * VideoRooms
        * VideoParticipants

4. Navado Wray: 
    * Create Flashcard component
    * Create Flashcard DB Model
    * Ablility to edit flashcards (add/delete/modify)

5. George Alvarado: 
    * Created all HTML functions
    * Created all CSS functionns 
    

