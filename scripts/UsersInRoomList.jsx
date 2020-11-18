import * as React from 'react';
import Socket from './Socket';

function UsersInRoomList() {
  const [users, setUsers] = React.useState([]);
  const [picUrls, setUrls] = React.useState([]);

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
      })
    });
  }

  getNewUser();

  return (
    <div className="UsersInRoomList">
      <ul className="userListing">
        <h1 className="UserTitle">Users:</h1>
        {
          users.map((user, index) => <li key={index}><img src={picUrls[index]} className="img"></img> {user}</li>)
        }
      </ul>
    </div>
  );
}

export default UsersInRoomList;
