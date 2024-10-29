import { HeatingSettings } from "./HeatingSettings";
import { useLogIn } from "./useLogIn";

function App() {

  const { logIn, logOut, isLoggedIn } = useLogIn();

 return (
    <div className="App">
      <h1>el-man web</h1>
      {
        isLoggedIn ? <button onClick={logOut}>Log out</button> : <button onClick={logIn}>Log in</button>
      }
      {
        isLoggedIn && <HeatingSettings />
      }
    </div>
  );
}

export default App;
