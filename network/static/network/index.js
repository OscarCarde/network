document.addEventListener('DOMContentLoaded', () => {
    

    let home_view = document.querySelector('#home-view');
    document.querySelectorAll(".shows-newpost-form").forEach(page => {
        page.addEventListener('click', () => {
            home_view.style.display = 'block';
        })
    })
})

//TODO: Hide new post form when on Following and Profile