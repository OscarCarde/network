const number_of_posts = 2;
let offset = 0

document.addEventListener('DOMContentLoaded', () => {
    

    let newpost_form = document.querySelector('#newpost-form');
    newpost_form.style.display = 'block';
    document.querySelector('#profile-button').addEventListener('click', () => loadPage('#profile'));
    //document.querySelector('#allposts-button').addEventListener('click', () => loadPage('#allposts'));
    document.querySelector('#following-button').addEventListener('click', () => loadPage('#following'));

    window.onscroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            loadPosts();
        }
    };

    loadPage('#allposts');
})

//TODO: loadPage
function loadPage(page) {
    //hide all the view divs except the element for the corresponding parameter
    document.querySelector('#profile').style.display = 'none';
    document.querySelector('#allposts').style.display = 'none';
    document.querySelector('#following').style.display = 'none';

    document.querySelector(`${page}`).style.display = 'grid';


    if(page === "#allposts") {
        document.querySelector('#newpost-form').style.display = 'block';
        loadPosts();
    }
    else {
        document.querySelector('#newpost-form').style.display = 'none';
    }


}

function loadPosts() {

    //load posts from /posts/ api
    fetch(`/posts?num_posts=${number_of_posts}&offset=${offset}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post)
    })

    offset += number_of_posts;
}

function add_post(contents) {
     //create post elements
    let post = document.createElement('li');
    let poster = document.createElement('h4');
    let text = document.createElement('p');
    let media = document.createElement('img');
    let timestamp = document.createElement('p');

    //populate post
    poster.innerHTML = contents.by;
    text.innerHTML = contents.content;
    media.src = contents.media;
    media.className = "post-media"  
    timestamp = contents.timestamp;

    post.className = 'post list-group-item';
    post.append(poster);
    if(contents.media) {
        post.append(media);
    }
    post.append(text);
    post.append(timestamp);

    document.querySelector('#allposts').append(post);
}