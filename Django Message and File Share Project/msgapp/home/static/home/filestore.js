var firebaseConfig = {
    apiKey: "AIzaSyAd9lY6vB_aaQwWi7frtMMgAlNjkAzoGKs",
    authDomain: "chatapp-ad441.firebaseapp.com",
    databaseURL: "https://chatapp-ad441-default-rtdb.firebaseio.com",
    projectId: "chatapp-ad441",
    storageBucket: "chatapp-ad441.appspot.com",
    messagingSenderId: "728979071113",
    appId: "1:728979071113:web:b861a30c5a6554c4636658"
  };
  // Initialize Firebase
firebase.initializeApp(firebaseConfig);

const db = firebase.database();
const msgRef = db.ref(table_name);

const msg = {
    message_type: 2,
    sender_phone_number: sender_number,
    text: file_name
};
setTimeout(() => {
    var it = msgRef.push(msg);
    window.location.href = refresh;
}, 1000);
