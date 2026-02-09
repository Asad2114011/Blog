// toggle like 
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        const icon = this.querySelector('i');
        const count = this.querySelector('.like-count');

        fetch(`/posts/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                } else {
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                }
                count.textContent = data.like_count;
            });
    });
});
// toggle bookmarked
document.querySelectorAll('.bookmark-btn').forEach(btn=>{
    btn.addEventListener('click',function(e){
        e.preventDefault();
        const postId=this.dataset.postId;
        const icon=this.querySelector('i');
        fetch(`/posts/bookmark/${postId}/`,{
            method:'POST',
            headers:{
                'X-CSRFToken':getCookie('csrftoken'),
            }
        })
            .then(response=>response.json())
            .then(data=>{
                if(data.bookmarked){
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                }else{
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                }
            });
    });
});


// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Toggle reply form
document.querySelectorAll('.reply-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        const replyForm = document.querySelector(`.reply-form-${commentId}`);
        replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
    });
});

// Cancel reply
document.querySelectorAll('.cancel-reply').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        document.querySelector(`.reply-form-${commentId}`).style.display = 'none';
    });
});

// Toggle edit form
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        document.querySelector(`.comment-content-${commentId}`).style.display = 'none';
        document.querySelector(`.edit-form-${commentId}`).style.display = 'block';
    });
});

// Cancel edit
document.querySelectorAll('.cancel-edit').forEach(btn => {
    btn.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        document.querySelector(`.comment-content-${commentId}`).style.display = 'block';
        document.querySelector(`.edit-form-${commentId}`).style.display = 'none';
    });
});

