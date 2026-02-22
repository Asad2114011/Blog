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
                showMessage(data.message,'success');
            }else{
                icon.classList.remove('fa-solid');
                icon.classList.add('fa-regular');
                showMessage(data.message,'info');
            }
        });
    });
});
// toggle reply form
document.querySelectorAll('.reply-btn').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment=this.dataset.commentId;
        const replyForm=document.querySelector(`.reply-form-${comment}`);
        replyForm.style.display=replyForm.style.display==='none'?'block':'none';
    });
});
// cancel reply
document.querySelectorAll('.cancel-reply').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment=this.dataset.commentId;
        document.querySelector(`.reply-form-${comment}`).style.display='none';
    });
});
// toggle edit form
document.querySelectorAll('.edit-btn').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment = this.dataset.commentId;
        const content=document.querySelector(`.comment-content-${comment}`);
        const editForm=document.querySelector(`.edit-form-${comment}`);
        editForm.style.display=editForm.style.display=='none'?'block':'none';
        content.style.display=editForm.style.display==='none'?'block':'none';
    });
});
// cancel edit
document.querySelectorAll('.cancel-edit').forEach(btn=>{
    btn.addEventListener('click',function(){
        const comment = this.dataset.commentId;
        document.querySelector(`.comment-content-${comment}`).style.display='block';
        document.querySelector(`.edit-form-${comment}`).style.display='none';
    });
});
// main comment
document.addEventListener('submit',function(event){
    const form = event.target;
    if(form.classList.contains('add-comment-form')){
        event.preventDefault();
        const post = form.dataset.postId;
        const comment = form.querySelector('textarea').value; 
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
    }
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
// delete post
document.addEventListener('click', function(event){
    if(event.target.closest('.delete-post-btn')){
        const btn = event.target.closest('.delete-post-btn');
        // console.log('Clicked post id:', btn.dataset.postId);
        event.preventDefault();
        if(!confirm('Delete this post permanently!')) return;

        const post = btn.dataset.postId;
        // console.log('post',post);

        fetch(`/posts/delete/${post}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data.success);
            if(data.success){
                showMessage(data.message, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showMessage(data.message, 'error');
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
                showMessage(data.message,'success');
                setTimeout(()=>location.reload(),1000);
            }else{
                showMessage(data.message,'error');
            }
        });
    }
});

