document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#submit-create-post').addEventListener('click', create_post);
    console.log("aa");
});


function create_post() {
    console.log("coucou");
    const new_post_content = document.querySelector('#post-content').value;
    fetch('/index', {
        method: "POST",
        body: JSON.stringify({
        content: new_post_content
      })
    })
    .then(response => {
        console.log("ZZZ")
        console.log(response)
        response.json()
    })
    .then(result => console.log(result))
    };


