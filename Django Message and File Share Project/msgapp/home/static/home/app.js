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

const msgTable = document.getElementById("messages-table"); //the <ul> that displays all the <li> msgs
const msgInput = document.getElementById("message-input"); //the input element to write messages
const msgBtn = document.getElementById("msgBtn"); //the Send button
const disappear_during_fileshare = document.getElementById("disappear-during-fileshare");
const disappear_during_messaging = document.getElementById("disappear-during-messaging");

const db = firebase.database();
const msgRef = db.ref(table_name);


function sendMessage(e){
    e.preventDefault();
    const text = msgInput.value;
  
      if(!text.trim()) return alert('Please type a message'); //no msg submitted
      const msg = {
          message_type: 1,
          sender_phone_number: sender_number,
          text: text
      };
  
      msgRef.push(msg);
      msgInput.value = "";
  }

msgBtn.addEventListener('click', sendMessage);

msgInput.addEventListener("keydown",function(event){
  if (event.keyCode == 18){
    console.log('event occured');
    event.preventDefault();
    msgBtn.click();
  }
})
const updateMsgs = data =>{
    const {message_type, sender_phone_number, text} = data.val(); //get name and text
      processed_text = text.replace(/\n/g,'<br>');
      console.log(sender_phone_number);

        var row = msgTable.insertRow(-1);
        cell1 = row.insertCell(0);
        cell1.setAttribute('class','message-left');
        cell1.setAttribute('align','left');
        cell2 = row.insertCell(1);
        cell2.setAttribute('class','message-right');
        cell2.setAttribute('align','right');
      if (sender_phone_number==sender_number){
        if (message_type == 1){
        const msg  = `<div class="message-right-div" align="left">${processed_text}</div>`;
        cell2.innerHTML = msg;
        }
        else{
          console.log('hello');
          const msg  = `<form method="GET" action="${download_url}">
          <b><input type="submit" name="file" style="cursor: pointer;" class="file-right-div" align="left" value="${processed_text}" title="Click to Download"></b></form>`;
          cell2.innerHTML = msg;
        }
      }
      else{
        if (message_type == 1){
          const msg = `<div class="message-left-div" align="left">${processed_text}</div>`;
          cell1.innerHTML = msg;
        }
        else{
          
          const msg  = `<form method="GET" action="${download_url}"> 
          <input type="submit" name="file" style="cursor: pointer;" class="file-left-div" align="left" value="${processed_text}" title="Click to Download"></form>`;
          cell1.innerHTML = msg;
      }
    }
    window.scrollTo({ left: 0, top: document.body.scrollHeight, behavior: "smooth" });
}

msgRef.on('child_added', updateMsgs);


function disappear_file_section(){
    disappear_during_fileshare.style.display = "block";
    disappear_during_messaging.style.display = "none";
}

function disappear_messaging_section(){
    disappear_during_fileshare.style.display = "none";
    disappear_during_messaging.style.display = "block";
}