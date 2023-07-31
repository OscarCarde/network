const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;


let page_number = 1;

document.addEventListener('DOMContentLoaded', () => {
    
    const profile_button = document.querySelector('#profile-button');
    if(profile_button) {
        profile_button.addEventListener('click', () => {
            loadPage('profile');
            loadProfile(loggedin_user);
        });
    }

    const following_button = document.querySelector('#following-button');
    if(following_button){
        following_button.addEventListener('click', () => loadPage('following'));
    }

    loadPage('allposts');
})


function loadPage(page) {

    //hide all the view divs except the element for the corresponding parameter
    document.querySelector('#posts').replaceChildren();
    const new_form = document.querySelector('#newpost-form');
    if(new_form){
        new_form.style.display = 'none';
    }
    document.querySelector('#profile').style.display = 'none';
    document.querySelector("#previous").style.display = "none";
    document.querySelector("#next").style.display = "block";

    page_number = 1;
    
    if(page === "allposts") {
        if(new_form){
            new_form.style.display = 'block';
        } 
        loadPosts("/posts");
        document.querySelector("#previous").addEventListener('click', () => {
            page_number--;
            loadPosts("/posts");
        });
        document.querySelector("#next").addEventListener('click', () => {
            page_number++;
            loadPosts("/posts");
        });

    } else if(page === "profile") {
        document.querySelector('#profile').style.display = 'grid';
        
    } else if(page === "following") {
        loadPosts("/following");
        document.querySelector("#previous").addEventListener('click', () => {
            page_number--;
            loadPosts("/following");
        });
        document.querySelector("#next").addEventListener('click', () => {
            page_number++;
            loadPosts("/following");
        });
    }
}

function createPost(contents) {
     //create post elements
    let post = document.createElement('li');
    let poster = document.createElement('h5');
    let text = document.createElement('p');
    let media = document.createElement('img');
    let timestamp = document.createElement('p');
    let likes = document.createElement('p');
    let like = document.createElement('button');
    let edit = document.createElement('button');

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
        if(loggedin_user) {
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
    }

    edit.innerHTML = "Edit";

    post.className = 'post list-group-item';
    post.append(poster);
    if(contents.media) {
        post.append(media);
    }
    post.append(text, timestamp, likes, like);

    if(loggedin_user === poster.innerHTML) {
        post.append(edit);
    }

    //display the edit form when edit is clicked
    edit.addEventListener('click', () => {
        edit_form = document.createElement('form');

        submit = document.createElement('input');
        submit.type = "submit";
        submit.name = "edit";

        textarea = document.createElement('textarea');
        textarea.innerHTML = text.innerHTML;

        edit_form.append(textarea, submit);
        edit_form.onsubmit = () => {
            // how to pass submitted form data to editPost()
            let new_content = textarea.innerHTML;
            editPost(contents, new_content);
            text.innerHTML = new_content;
        };

        text.replaceWith(edit_form);

        //remove the form if click outside the post
        const replaceForm = function(event) {
            if (!post.contains(event.target) && event.target !== submit) {
                edit_form.replaceWith(text);
                document.removeEventListener('click', replaceForm);
              }
            
        }
        document.addEventListener('click', replaceForm);
    });


    return post;
}

function loadProfile(username) {
    document.querySelector("#previous").addEventListener('click', () => {
        page_number--;
        loadPosts("/posts/${username}", page_number);
        
    });
    document.querySelector("#next").addEventListener('click', () => {
        page_number++;
        loadPosts("/posts", page_number);
    });
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
        following.innerHTML = "Following " + data.profile.number_followed;
        following.id = "following";

        let followers = document.createElement('p');
        followers.innerHTML = "Followers " + data.profile.number_of_followers;
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
        if(!data.has_next){
            document.querySelector("#next").style.display = "none";
        } else {
            document.querySelector("#next").style.display = "block";
        }
        if(!data.has_previous){
            document.querySelector("#previous").style.display = "none";
        } else {
            document.querySelector("#previous").style.display = "block";
        }
        document.querySelector('#posts').replaceChildren();
        data.posts.forEach(post => {
            document.querySelector('#posts').append(createPost(post));
            window.scrollTo(0, 0);
        })
    })
    
}

function editPost(post, new_content) {
    //TODO
    console.log(new_content + " loaded");
    fetch(`/edit/${post.id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "new_content": new_content
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.edited);
    })
}