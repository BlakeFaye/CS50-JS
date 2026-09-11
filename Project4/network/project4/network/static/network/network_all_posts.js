document.addEventListener('DOMContentLoaded', function() {
    load_posts();
});

function load_posts(){

  fetch(`/all_posts_data`)
    .then(response => response.json())
    .then(posts =>
        {
            const post_table = document.createElement('table');
            post_table.className = 'post_table';
            const post_table_body = document.createElement('tbody');
            post_table.appendChild(post_table_body)

            for (let i = 1; i < posts.length; i++)
            {
                const single_post = posts[i]
                const single_post_data = [single_post.content, single_post.user, single_post.timestamp]
                console.log(single_post_data)

                const post_table_row = document.createElement('tr');
                post_table_row.className = 'mail_table_row';
                
                //display post details in a row
                single_post_data.forEach(item => {
                    //Cells
                    const post_table_cell = document.createElement('td');
                    post_table_cell.textContent = item
                    post_table_cell.className = 'post_table_cell';
                    post_table_row.appendChild(post_table_cell)
                });

                //display post actions in a row
                const post_action = document.createElement('td');

                //Like logic
                const like_counter = document.createElement('td');
                const like_button = document.createElement('button');
                function update_like_display(){
                    fetch(`/total_likes/${single_post.id}`)
                    .then(response => response.json())
                    .then(single_like_counter => {
                        // Like counter and button text
                        const like_counter_value = single_like_counter.total_likes
                        console.log(like_counter_value, single_post)
                        like_counter.innerHTML = `Likes: ${like_counter_value}`

                        if (like_counter_value > 0) {
                            console.log("UNLIKE")
                            like_button.innerHTML = "Unlike this post";
                        }
                        else {
                            console.log("LIKE")
                            like_button.innerHTML = "Like this post";
                        }
                        post_action.appendChild(like_counter)
                    })
                }
                update_like_display();
                                            
                // Like logic              
                like_button.addEventListener('click', function() {
                    fetch(`/like_post/${single_post.id}`)
                    .then(response => response.json)
                    .then(result => update_like_display())                    
                })
               
                post_action.appendChild(like_button)

                //post edit logic
                const edit_button = document.createElement('button');
                edit_button.innerHTML = "Edit this post";
                post_action.appendChild(edit_button)

                post_table_row.appendChild(post_action)

                //display a complete row
                post_table_body.appendChild(post_table_row);

                document.querySelector('#all-posts-view').append(post_table);
            }   
        }
    )
}
