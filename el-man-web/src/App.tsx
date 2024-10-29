import { useFirestore } from "./useFirestore";
import { useLogIn } from "./useLogIn";

function App() {

  const { logIn, logOut, isLoggedIn} = useLogIn();

  // TODO: add authentication + rules to firestore
  //const { getHeatingSettings } = useFirestore();
  //console.log(getHeatingSettings());
  return (
    <div className="App">
      {
        isLoggedIn ? <button onClick={logOut}>Log out</button> : <button onClick={logIn}>Log in</button>

      }
      
      el-man-web
    </div>
  );
}

export default App;
