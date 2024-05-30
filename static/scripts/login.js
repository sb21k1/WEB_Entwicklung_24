// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getDatabase, set, ref, update } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCvaudn5y9Lc7sB1U7b3iJNh1OhMgilmis",
    authDomain: "places-de11a.firebaseapp.com",
    databaseURL: "https://places-de11a-default-rtdb.firebaseio.com",
    projectId: "places-de11a",
    storageBucket: "places-de11a.appspot.com",
    messagingSenderId: "270159356467",
    appId: "1:270159356467:web:836fcefca3437bf397b946"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth();

document.getElementById('signup').addEventListener('click', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const full_name = document.getElementById('full_name').value;

    if (!email || !password || !full_name) {
        alert('Please fill all fields');
        return;
    }

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            // Write user data to the database
            set(ref(db, 'users/' + user.uid), {
                fullName: full_name,
                email: email
            });
            alert('User created successfully');
        })
        .catch((error) => {
            const errorMessage = error.message;
            alert(errorMessage);
        });
});

document.getElementById('login').addEventListener('click', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert('Please fill all fields');
        return;
    }

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            // Update last login
            update(ref(db, 'users/' + user.uid), {
                last_login: new Date().toISOString()
            });
            alert('User logged in successfully');
        })
        .catch((error) => {
            const errorMessage = error.message;
            alert(errorMessage);
        });
});