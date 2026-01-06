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

  // Compose mail
  // Adblockers must be unabled for the composition form to work
  document.querySelector('#submit-compose-form').onclick = () => {
    const new_mail_recipients = document.querySelector('#compose-recipients').value;
    const new_mail_subject = document.querySelector('#compose-subject').value;
    const new_mail_body = document.querySelector('#compose-body').value;

    //Get a list of all recipients
    var recs = new_mail_recipients.split(", ");
    
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
  //Display the mail viewer and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-mail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${mail_id}`)
    .then(response => response.json())
    .then(email => {

      //Display mail infos
      document.querySelector('#single-mail-view').innerHTML = 
      `
      <p> Single email view </p>
      <p> Subject : ${email.subject}</p>
      <p> Sender : ${email.sender}</p>
      <p> Recipients : ${email.recipients}</p>
      <p> Timestamp : ${email.timestamp}</p>
      <p> Body : ${email.body}</p>
      <p> Read? : ${email.read} | Archived? : ${email.archived}</p>
      <p> BBBBBBB </p>
      `;

      //Switch to read
      if (!email.read){
        fetch(`/emails/${mail_id}`,{
        method: "PUT",
        body: JSON.stringify({
          read: true
        })
        }
      )
      }

      //Archive logic
      const archive_button = document.createElement('button');
      if (email.archived) {
        archive_button.innerHTML = "Unarchive";
        archive_button.addEventListener('click', function() {
            fetch(`/emails/${mail_id}`,{
              method: "PUT",
              body: JSON.stringify({
                archived: false
              })
            })
            .then(() => {load_mailbox('inbox')})
        })
      } 

      else {
        archive_button.innerHTML = "Archive";
        archive_button.addEventListener('click', function() {
            fetch(`/emails/${mail_id}`,{
              method: "PUT",
              body: JSON.stringify({
                archived: true
              })
            })
            .then(() => {load_mailbox('archive')})
        })
      }
      
      //Reply logic
      const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      reply_button.addEventListener('click', function() {
        compose_email()
        document.getElementById('page_title').innerHTML  = 'Reply';
        if (email.subject.substring(0,3) == 'Re:')
        {
          document.querySelector('#compose-subject').value = email.subject;
        }
        else{
          document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
        }
        document.querySelector('#compose-recipients').value = email.recipients;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \r\n${email.body}`;
      })

    document.querySelector('#single-mail-view').append(archive_button);
    document.querySelector('#single-mail-view').append(reply_button);
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
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails =>
      {
      if (emails.length == 0) {
        document.querySelector('#emails-view').innerHTML = document.querySelector('#emails-view').innerHTML  + "No mails to display"
      }
      else {
        //Mail table building
      const mail_table = document.createElement('table');
      mail_table.className = 'mail_table';
      const mail_table_body = document.createElement('tbody');
      mail_table.appendChild(mail_table_body)

        for (let i = 0; i < emails.length ; i++) {
          //Rows
          const mel = emails[i];
          const mel_data = [mel.sender, mel.subject, mel.timestamp]
          
          const mail_table_row = document.createElement('tr');
          mail_table_row.className = 'mail_table_row';

          mel_data.forEach(item => {
            //Cells
            const mail_table_cell = document.createElement('td');
            mail_table_cell.textContent = item
            mail_table_cell.className = 'mail_table_cell';
            mail_table_row.appendChild(mail_table_cell)
          });

          mail_table_body.appendChild(mail_table_row)

          if (mel.read) {
            mail_table_row.className = "read"
          };

          mail_table_row.addEventListener('click', function() {
            view_mail(mel.id)
          })

          document.querySelector('#emails-view').append(mail_table);
        }
         
      }
    }
  )
    }
  