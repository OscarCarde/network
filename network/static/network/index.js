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
    document.querySelectorAll(".username").forEach(element =>{
        element.addEventListener('click', () =>{ 
            loadPage('#profile');
            loadProfile(element.innerHTML);
        })
    })
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
        data.posts.forEach(post => {
            post_element = add_post(post);
            document.querySelector('#allposts').append(post_element);
        })
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
    poster.className = "clickable";
    poster.addEventListener('click', () =>{ 
        loadPage('#profile');
        loadProfile(poster.innerHTML);
    })
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

    return post;
}

function loadProfile(username) {
    fetch(`/profile?username=${username}`)
    .then(response => response.json())
    .then(data => {
        
        media = document.createElement('img');
        media.src = data.profile.profile_picture;


        user_name = document.createElement('h3');
        user_name.innerHTML = data.profile.username;

        
        follow = document.querySelector("#follow");
        if(data.profile.is_following) {
            follow.innerHTML = "Unfollow";
        } else {
            follow.innerHTML = "Follow";
        }

        if(loggedin_user === user_name.innerHTML) {
            follow.style.display = "none";
        } else {
            follow.style.display = "block";
        }

        following = document.createElement('p');
        following.innerHTML = "Following: " + data.profile.number_followed;
        following.id = "following";

        followers = document.createElement('p');
        followers.innerHTML = "Followers: " + data.profile.number_followed;
        followers.id = "followers";

        about = document.createElement('p');
        about.innerHTML = data.profile.about;
        about.id = "profile-status";

        document.querySelector("#profile-picture").replaceChildren(media);
        document.querySelector("#profile-info").replaceChildren(user_name, following, followers, about);

        document.querySelector('#profile-posts').replaceChildren();
        data.profile.ordered_posts.forEach(post => {
            post_element = add_post(post);
            document.querySelector('#profile-posts').append(post_element);
        });
    })
}