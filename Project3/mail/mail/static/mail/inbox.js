document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
 
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  loop1: for (let i = 1; i<10; i++) //i<100 T-T
    {
      
      fetch(`/emails/${i}`)
      .then(response => response.json())
      .then(email => {
      console.log(email);
      console.log(i)
      //console.log(email.hasOwnProperty("error"));
      if (email.hasOwnProperty("error")){
        console.log("coucou");
      }
    })
      }

      
  fetch('/emails/1')
  .then(response => response.json())
  .then(email => {
    console.log(email);

    //if error key found in returned JSON print it
    if (email.hasOwnProperty("error")){ 
      console.log(email.error);
      document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML + "Error: " + email.error;
    }
    //otherwise, print mails
    else { 
      const mel = email;
      const read = "No";
      const archived = "No";
      if (mel.read) {
        read = "Yes"
      }
      if (mel.archived) {
        read = "Yes"
      }

      document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  +  
      `<p> Subject : ${mel.subject}</p>
      <p> Sender : ${mel.sender}</p>
      <p> Timestamp : ${mel.timestamp}</p>
      <p> Body : ${mel.body}</p>
      <p> Read? : ${read} | Archived? : ${archived}</p>
      ____________
      `
    }
    document.createElement("h4").innerHTML = email
  }
  )
}