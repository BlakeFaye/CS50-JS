document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#create-post-view').style.display = 'none';
    document.querySelector('#create-post-button').addEventListener('click', create_post);
});

function load_posts() {
    console.log("placholder for posts")
}

function create_post() {
    document.querySelector('#create-post-view').style.display = 'block';
    
    //back to main page logic
    document.querySelector('#cancel-post-button').onclick = () => {
        document.querySelector('#create-post-view').style.display = 'none';
    }

    //submit create post form
    document.querySelector('#submit-create-post').onclick = () => {
        const new_post_content = document.querySelector('#post-content').value;
        fetch('/add_post', {
            method: "POST",
            body: JSON.stringify({
            content: new_post_content
        })
        })
        .then(response => response.json())
        .then(result => console.log(result))
    };
}

