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

                single_post_data.forEach(item => {
                    //Cells
                    const post_table_cell = document.createElement('td');
                    post_table_cell.textContent = item
                    post_table_cell.className = 'post_table_cell';
                    post_table_row.appendChild(post_table_cell)
                });

                post_table_body.appendChild(post_table_row);

                document.querySelector('#all-posts-view').append(post_table);
            }   
        }
    )
}
