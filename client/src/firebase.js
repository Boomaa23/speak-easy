import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyD336oBfwhFc8NEh5nSxpjOv4YowFLfs_s",
  authDomain: "inventory-a7bb6.firebaseapp.com",
  projectId: "inventory-a7bb6",
  storageBucket: "inventory-a7bb6.appspot.com",
  messagingSenderId: "515957941591",
  appId: "1:515957941591:web:82b2ff7abd3e688d3cca12",
  measurementId: "G-NXDVPVWHJK"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup };
