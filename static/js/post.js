// get csrf token
function getCookie(val){
    let cookie=null;
    if(document.cookie && document.cookie!=null){
        const cookies=document.cookie.split(';');
        for(let i=0;i<cookies.length;i++){
            const x=cookies[i].trim();
            const cur=x.substring(0,val.length +1);
            if(cur==(val+'=')){
                cookie=x.substring(cur.length);
                cookie=decodeURIComponent(cookie);
                break;
            }
        }
    }
    return cookie;
}
// toggle like 
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        const postId=this.dataset.postId;
        const icon=this.querySelector('i');
        const count=this.querySelector('.like-count');

        fetch(`/posts/like/${postId}/`,{
            method:'POST',
            headers:{
                'X-CSRFToken':getCookie('csrftoken'),
            }
        })
        .then(response=>response.json())
        .then(data=>{
            if (data.liked){
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
// toggle reply form
document.querySelectorAll('.reply-btn').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment=this.dataset.comment;
        const replyForm=document.querySelector(`.reply-form-${comment}`);
        replyForm.style.display=replyForm.style.display==='none'?'block':'none';
    });
});

// cancel reply
document.querySelectorAll('.cancel-reply').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment=this.dataset.comment;
        document.querySelector(`.reply-form-${comment}`).style.display='none';
    });
});

// toggle edit form
document.querySelectorAll('.edit-btn').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment = this.dataset.comment;
        const content=document.querySelector(`.comment-content-${comment}`);
        const editForm=document.querySelector(`.edit-form-${comment}`);
        editForm.style.display=editForm.style.display=='none'?'block':'none';
        content.style.display=editForm.style.display==='none'?'block':'none';
    });
});
// cancel edit
document.querySelectorAll('.cancel-edit').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment = this.dataset.comment;
        document.querySelector(`.comment-content-${comment}`).style.display='block';
        document.querySelector(`.edit-form-${comment}`).style.display='none';
    });
});
// main comment
const commentForm=document.querySelector('.add-comment-form');
commentForm.addEventListener('submit',function(event){
    event.preventDefault();
    const post=this.dataset.postId;
    const comment=this.querySelector('textarea').value; 
    fetch(`/posts/comment/${post}/`,{
        method:'POST',
        headers:{
            'X-CSRFToken':getCookie('csrftoken'),
            'Content-Type':'application/x-www-form-urlencoded',
        },
        body:`content=${encodeURIComponent(comment)}`
    }).then(response=>response.json()).then(data=>{
        if(data.success){
            location.reload();
        }
    });
});
// reply comment
document.addEventListener('submit',function(event){
    const form=event.target;
    if(form.classList.contains('add-reply-form')){
        event.preventDefault();
        const parent_comment=form.dataset.commentId;
        const reply_comment=form.querySelector('textarea').value;

        fetch(`/posts/comment/reply/${parent_comment}/`,{
            method:'POST',
            headers:{
                'X-CSRFToken':getCookie('csrftoken'),
                'Content-Type':'application/x-www-form-urlencoded',
            },
            body:`content=${encodeURIComponent(reply_comment)}`
        }).then(response=>response.json()).then(data=>{
            if(data.success){
                location.reload();
            }
        });
    }
});

// edit comment 
document.addEventListener('submit',function(event){
    const form=event.target;
    if(form.classList.contains('edit-comment-form')){
        event.preventDefault();
        const comment=form.dataset.commentId;
        const content=form.querySelector('textarea').value;

        fetch(`/posts/comment/edit/${comment}/`,{
            method:'POST',
            headers:{
                'X-CSRFToken':getCookie('csrftoken'),
                'Content-Type':'application/x-www-form-urlencoded',
            },
            body:`content=${encodeURIComponent(content)}`,
        }).then(response=>response.json()).then(data=>{
            if(data.success){
                location.reload();
            }
        });
    }
});

// delete comment 
document.addEventListener('click',function(event){
    const form=event.target;
    if(form.closest('.delete-comment')){
        event.preventDefault();
        if(!confirm('Delete this comment?'))return;
        const comment=form.dataset.commentId;

        fetch(`/posts/comment/delete/${comment}/`,{
            method:'POST',
            headers:{
                'X-CSRFToken':getCookie('csrftoken'),
            }
        }).then(response=>response.json()).then(data=>{
            if(data.success){
                location.reload();
            }
        });
    }
});

