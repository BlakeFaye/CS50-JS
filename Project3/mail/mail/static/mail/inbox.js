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
  document.querySelector('#single-mail-view').style.display = 'none';
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

    // pour que ça fonctionne, il faut désactiver ublock et abp
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

function view_mail(mail_id){
  console.log (mail_id)

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-mail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${mail_id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email)
        document.querySelector('#single-mail-view').innerHTML = 
      `
      <p> Single email view </p>
      <p> Subject : ${email.subject}</p>
      <p> Sender : ${email.sender}</p>
      <p> Timestamp : ${email.timestamp}</p>
      <p> Body : ${email.body}</p>
      <p> Read? : ${email.read} | Archived? : ${email.archived}</p>
      <p> BBBBBBB </p>
      `;

    if (!email.read){
      fetch(`/emails/${mail_id}`,{
      method: "PUT",
      body: JSON.stringify({
        read: true
      })
      }
    )
    }

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#single-mail-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    }
  )
}

function load_mailbox(mailbox) {
 
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#single-mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  // help : https://github.com/kazimovzaman2/CS50w-Mail/blob/main/mail/static/mail/inbox.js
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  console.log("mailbox: " + mailbox)


  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails =>
      {
      if (emails.length == 0) {
        document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  + "No mails to display"
      }
      for (let i = 0; i < emails.length ; i++) {
        console.log(emails[i])
        const mel = emails[i];
    
        const single_mail = document.createElement('div');
        single_mail.innerHTML = 
      `<p> Subject : ${mel.subject}</p>
      <p> Sender : ${mel.sender}</p>
      <p> Timestamp : ${mel.timestamp}</p>
      <p> Body : ${mel.body}</p>
      <p> Read? : ${mel.read} | Archived? : ${mel.archived}</p>
      ____________
      `
      if (mel.read) {
        single_mail.className = "read"
      };

      single_mail.addEventListener('click', function() {
        view_mail(mel.id)
      })

      document.querySelector('#emails-view').append(single_mail);
      }
    }
  )
    }
  