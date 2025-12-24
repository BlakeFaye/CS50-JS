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

  document.querySelector('#submit-compose-form').onclick = () => {
    const new_mail_recipients = document.querySelector('#compose-recipients').value;
    const new_mail_subject = document.querySelector('#compose-subject').value;
    const new_mail_body = document.querySelector('#compose-body').value;

    console.log (new_mail_subject);
    console.log (new_mail_recipients);
    console.log (new_mail_body);

    var recs = new_mail_recipients.split(", ");
    console.log(recs);

    // TODO : event.preventDefault empêcherait l'exécution du fetch
    // https://cs50.stackexchange.com/questions/43868/cs50w-mail-javascript-function-only-working-on-chrome
    // https://stackoverflow.com/questions/7056669/how-to-prevent-default-event-handling-in-an-onclick-method
    fetch('/emails',{
      method: "POST",
      body: JSON.stringify({
        recipients: new_mail_recipients,
        subject: new_mail_subject,
        body: new_mail_body
      })
    })
    .then(response => response.json())
    .then(result => console.log(result))
    };
}

function load_mailbox(mailbox) {
 
  console.log("beginning of load_mailbox")
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  console.log("mailbox: " + mailbox)

  fetch('/emails/inbox')
    .then(response => response.json())
    .then(email => {
      if (email.length == 0) {
        document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  + "No mails to display"
      }
      for (let i = 0; i < email.length ; i++) {
        console.log(email[i])
        const mel = email[i];
        //TODO : transcoder les true/false des read et archived
        // const read = "No";
        // const archived = "No";
        // if (mel.read) {
        //   read = "Yes"
        // }
        // if (mel.archived) {
        //   read = "Yes"
        // }
        console.log("sent " + mel.sent + " " + mel.id)
        console.log("archived " + mel.archived + " " + mel.id)
        console.log("mailbox " + mailbox)
        if (mailbox = 'sent' && mel.sent) {
           document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  +  
      `<p> Subject : ${mel.subject}</p>
      <p> Sender : ${mel.sender}</p>
      <p> Timestamp : ${mel.timestamp}</p>
      <p> Body : ${mel.body}</p>
      <p> Read? : ${mel.read} | Archived? : ${mel.archived}</p>
      ____________
      `
        }
        else if (mailbox = 'archive' && mel.archived) {
           document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  +  
      `<p> Subject : ${mel.subject}</p>
      <p> Sender : ${mel.sender}</p>
      <p> Timestamp : ${mel.timestamp}</p>
      <p> Body : ${mel.body}</p>
      <p> Read? : ${mel.read} | Archived? : ${mel.archived}</p>
      ____________
      `
        }
        else {
          document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  +  
      `<p> Subject : ${mel.subject}</p>
      <p> Sender : ${mel.sender}</p>
      <p> Timestamp : ${mel.timestamp}</p>
      <p> Body : ${mel.body}</p>
      <p> Read? : ${mel.read} | Archived? : ${mel.archived}</p>
      ____________
      `
        }
      }
    })


    }
  