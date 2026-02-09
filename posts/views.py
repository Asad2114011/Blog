from django.shortcuts import render,redirect
from .import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_like(request,id):
    post = models.Post.objects.get(id=id)
    author = request.user.author_profile
    
    like = models.Like.objects.filter(post=post, user=author)
    
    if like.exists():
        like.delete()
        liked = False
    else:
        models.Like.objects.create(post=post, user=author)
        liked = True
    
    return JsonResponse({'liked': liked,'like_count': post.likes.count()})


@login_required
@require_POST
def toggle_bookmark(request,id):
    post=models.Post.objects.get(id=id)
    author=request.user.author_profile
    bookmark=models.Bookmark.objects.filter(post=post,user=author)

    if bookmark.exists():
        bookmark.delete()
        bookmarked=False
    else:
        models.Bookmark.objects.create(post=post,user=author)
        bookmarked=True
    return JsonResponse({'bookmarked':bookmarked})


@csrf_exempt
def tinymce_upload(request):
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        
        upload_path = os.path.join(settings.MEDIA_ROOT, 'tinymce')
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        file_url = os.path.join(settings.MEDIA_URL, 'tinymce', file.name)
        return JsonResponse({'location': file_url})
    
    return JsonResponse({'error': 'Upload failed'}, status=400)


@login_required
def create_post(request):
    if request.method=='POST':
        post_form=forms.PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            post.author=request.user.author_profile
            post.save()
            post_form.save_m2m()
            return redirect('profile')
    else:
        post_form=forms.PostForm()
    return render(request,'create_post.html',{'form':post_form})

@login_required
def post_details(request,slug):
    post=models.Post.objects.get(slug=slug)

    post.view_count+=1
    post.save(update_fields=['view_count'])

    user_liked=False
    user_commented=False
    user_bookmarked=False

    if request.user.is_authenticated:
        user_liked=post.likes.filter(user=request.user.author_profile).exists()
        user_commented=post.comments.filter(user=request.user.author_profile).exists()
        user_bookmarked=post.bookmarks.filter(user=request.user.author_profile).exists()
        
    return render(request,'post_details.html',{'post':post,'user_liked':user_liked,'user_commented':user_commented,'user_bookmarked':user_bookmarked})

@login_required
def edit_post(request,id):
    post =models.Post.objects.get(pk=id)
    post_form=forms.PostForm(instance=post)

    if request.method=='POST':
        post_form=forms.PostForm(request.POST,request.FILES,instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('home')
   
    return render(request,'edit_post.html',{'form':post_form})

@login_required
def delete_post(request,id):
     post =models.Post.objects.get(pk=id)
     post.delete()
     return redirect('home')

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = models.Post.objects.get(id=post_id)
        content = request.POST.get('content')
        
        models.Comment.objects.create(
            post=post,
            user=request.user.author_profile,
            content=content
        )
    
    return redirect('post_details', slug=post.slug)

@login_required
def add_reply(request, comment_id):
    if request.method == 'POST':
        parent_comment = models.Comment.objects.get(id=comment_id)
        content = request.POST.get('content')
        
        models.Comment.objects.create(
            post=parent_comment.post,
            user=request.user.author_profile,
            content=content,
            parent=parent_comment
        )
    
    return redirect('post_details', slug=parent_comment.post.slug)

@login_required
def edit_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    
    if request.user.author_profile == comment.user:
        if request.method == 'POST':
            comment.content = request.POST.get('content')
            comment.save()
    
    return redirect('post_details', slug=comment.post.slug)

@login_required
def delete_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    post_slug = comment.post.slug
    
    if request.user.author_profile == comment.user:
        comment.delete()
    
    return redirect('post_details', slug=post_slug)