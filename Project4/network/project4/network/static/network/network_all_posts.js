document.addEventListener('DOMContentLoaded', function() {
    load_posts();
});

function load_posts(){
    document.querySelector('#all-posts-view').style.display = 'block';

  fetch(`/all_posts_data`)
    .then(response => response.json())
    .then(posts =>
        {
            for (let i = 0; i < posts.length; i++)
            {
                console.log(i)
                console.log(posts[i])
            }
            
        }
    )
}

function view_post(post_id){
    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(post => {
        document.querySelector('#all-posts-view').innerHTML = 
      `
      <p> Single post view </p>
      <p> Content : ${post.content}</p>
      <p> Timestamp : ${post.timestamp}</p>
      <p> BBBBBBB </p>
      `;
    })
}