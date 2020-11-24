import * as React from 'react';
import Socket from './Socket';

function UsersInRoomList() {
  const [users, setUsers] = React.useState([]);
  const [picUrls, setUrls] = React.useState([]);
  const [userIds, setIds] = React.useState([]);

  function updateUsers(data) {
    console.log(`Received new user: ${data.all_users}`);
    setUsers(data.all_users);
    setUrls(data.all_user_pics);
  }

  function getNewUser() {
    React.useEffect(() => {
      Socket.on('users received', (data) => {
        setUsers(data.all_users);
        setUrls(data.all_user_pics);
        setIds(data.all_user_ids);
      });
    });
  }
  
  function kickUser(kickTargetId) {
    Socket.emit("kick user request", {
      kickedUserId: kickTargetId,
    });
    
  }

  getNewUser();

  return (
    <div className="container userListing">
      <div className="userListing">
        {
          users.map((user, index) => 
          <div id="user" key={index}>
            <img src={picUrls[index]} className="img"></img>
            <p>{user}</p>
            <button onClick={(event) => kickUser(userIds[index][0])} type="submit">Kick</button>
          </div>)
        }
      </div>
    </div>
  );
}

export default UsersInRoomList;

// this fails: users.map((user,index) => <div id="user" key={index}><img src={picUrls[index]}/></div>)
