// Import and configure the Firebase SDK
// These scripts are made available when the app is served or deployed on Firebase Hosting
// If you do not want to serve/host your project using Firebase Hosting see https://firebase.google.com/docs/web/setup
importScripts('https://www.gstatic.com/firebasejs/4.1.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.1.1/firebase-messaging.js');
importScripts('https://www.gstatic.com/firebasejs/4.1.1/firebase.js');

 var config = {
    apiKey: "AIzaSyB6Krmsq2qeDj2G7rNJZkFsiGZmYytDQnM",
    authDomain: "pmonesims.firebaseapp.com",
    databaseURL: "https://pmonesims.firebaseio.com",
    projectId: "pmonesims",
    storageBucket: "pmonesims.appspot.com",
    messagingSenderId: "1024527895183"
  };
  firebase.initializeApp(config);
firebase.messaging();
