let page_number = 1;
//variables for posts infinite scroll

document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#profile-button').addEventListener('click', () => {
        loadPage('profile');
        loadProfile(loggedin_user);
    });
    document.querySelector('#following-button').addEventListener('click', () => loadPage('following'));


    loadPage('allposts');
})

//TODO: loadPage
function loadPage(page) {

    //hide all the view divs except the element for the corresponding parameter
    document.querySelector('#posts').replaceChildren();
    document.querySelector('#newpost-form').style.display = 'none';
    document.querySelector('#profile').style.display = 'none';

    page_number = 1;
    
    if(page === "allposts") {
        document.querySelector('#newpost-form').style.display = 'block';
        loadPosts("/posts");

    } else if(page === "profile") {
        document.querySelector('#profile').style.display = 'grid';

    } else if(page === "following") {
        loadPosts("/following");
    }
}

function loadAllPosts() {

    //load posts from /posts/ api
    fetch(`/posts?${page_number}`)
    .then(response => response.json())
    .then(data => {
        page_number ++;
        data.posts.forEach(post => {
            post_element = add_post(post);
            document.querySelector('#posts').append(post_element);
        })
    })
}

//function

function add_post(contents) {
     //create post elements
    let post = document.createElement('li');
    let poster = document.createElement('h4');
    let text = document.createElement('p');
    let media = document.createElement('img');
    let timestamp = document.createElement('p');
    let likes = document.createElement('p');
    let like = document.createElement('button');

    //populate post
    poster.innerHTML = contents.by;
    poster.className = "clickable";
    poster.addEventListener('click', () =>{ 
        loadPage('profile');
        loadProfile(poster.innerHTML);
    })
    text.innerHTML = contents.content;
    media.src = contents.media;
    media.className = "post-media"  
    timestamp = contents.posted_since;
    likes.innerHTML = "Liked " + contents.likes
    like.innerHTML = "Like";

    like.onclick = () => {
        if(!contents.liked) {
            likes.innerHTML = "Liked " + (contents.likes + 1);
        } else {
            likes.innerHTML = "Liked " + (contents.likes -1);
        }
        fetch(`like/${contents.id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })

    }

    post.className = 'post list-group-item';
    post.append(poster);
    if(contents.media) {
        post.append(media);
    }
    post.append(text, timestamp, likes, like);

    return post;
}

function loadProfile(username) {
    fetch(`/profile?username=${username}&page=${page_number}`)
    .then(response => response.json())
    .then(data => {
        let media = document.createElement('img');
        media.src = data.profile.profile_picture;


        let user_name = document.createElement('h3');
        user_name.innerHTML = data.profile.username;

        
        let follow = document.querySelector("#follow");
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

        let following = document.createElement('p');
        following.innerHTML = "Following: " + data.profile.number_followed;
        following.id = "following";

        let followers = document.createElement('p');
        followers.innerHTML = "Followers: " + data.profile.number_of_followers;
        followers.id = "followers";

        let about = document.createElement('p');
        about.innerHTML = data.profile.about;
        about.id = "profile-status";

        document.querySelector("#profile-picture").replaceChildren(media);
        document.querySelector("#profile-info").replaceChildren(user_name, following, followers, about);
    })

    let follow = document.querySelector("#follow");
    follow.addEventListener('click', element => {

        if (follow.innerHTML === "Follow") {
            follow.innerHTML = "Unfollow";
        } else if (follow.innerHTML === "Unfollow") {
            follow.innerHTML = "Follow";
        }
        
        fetch(`follow/${username}`)
        .then(response => response.json())
        .then(status => {
            if(status.followed) {
                element.innerHTML = "Unfollow";
            } else if (!status.followed) {
                element.innerHTML = "Follow"
            }
        })
    })

    loadPosts(`/posts/${username}`);
}

function loadPosts(api_route) {
    fetch(`${api_route}?page=${page_number}`)
    .then(response => response.json())
    .then(data => {
        page_number ++;
        data.posts.forEach(post => {
            post_element = add_post(post);
            document.querySelector('#posts').append(post_element);
        })
    })
}