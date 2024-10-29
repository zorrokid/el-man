import { getAuth ,GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
import { useState } from "react";
export const useLogIn = () => {
    const [token, setToken] = useState<string | undefined>(undefined);
    const auth = getAuth();
    const provider = new GoogleAuthProvider();

    const logIn = () => {
        signInWithPopup(auth, provider)
        .then((result) => {
            // This gives you a Google Access Token. You can use it to access the Google API.
            const credential = GoogleAuthProvider.credentialFromResult(result);
            if (!credential) {
            console.log('credential is null');
            return;
            }
            const token = credential.accessToken;
            setToken(token);
            // The signed-in user info.
            const user = result.user;
            // IdP data available using getAdditionalUserInfo(result)
            // ...
            console.log('user', user);
        }).catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            const errorMessage = error.message;
            // The email of the user's account used.
            const email = error.customData.email;
            // The AuthCredential type that was used.
            const credential = GoogleAuthProvider.credentialFromError(error);
            // ...
            console.log(error)
        });
    }

    const logOut = () => {
        signOut(auth).then(() => {
            console.log('sign out');
            setToken(undefined);
        }).catch((error) => {
            console.log('sign out error', error);  
        });
    }

    return { logIn, logOut, token, isLoggedIn: token !== undefined };

}