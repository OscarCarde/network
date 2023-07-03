document.addEventListener('DOMContentLoaded', () => {
    
    let new_post_form = document.querySelector('#new-post-form');
    document.querySelector("#all-posts-button").addEventListener('click', () => {
        if(!!new_post_form){
            event.preventDefault();
            new_post_form.style.display = 'block';  
        }
    });
    new_post_form.style.display = 'none';  
})
